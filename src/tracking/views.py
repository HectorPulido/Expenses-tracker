import csv
import json
import base64
import datetime
from io import BytesIO

from django.db.models import Sum, Case, When, FloatField, Min, Max
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from wordcloud import WordCloud

from .forms import ExpenseForm
from .models import Expense, Category


# Handle user login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
        messages.error(request, "Invalid username or password")
    return render(request, "expenses/login.html")


# Handle user logout
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def index(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            form.save_m2m()
            return redirect("index")

    form = ExpenseForm(user=request.user)
    # ---------------------------------------------------
    # 1) Get last 7 days of raw expenses/incomes
    today = timezone.now().date()
    week_ago = today - datetime.timedelta(days=6)
    expenses = (
        Expense.objects.filter(user=request.user, issue_date__date__gte=week_ago)
        .prefetch_related("categories")
        .order_by("-issue_date", "-date_reg")
    )

    # 2) Build daily aggregates for chart
    qs = expenses  # same queryset, already filtered last 7d
    daily_qs = (
        qs.annotate(day=TruncDate("issue_date"))
        .values("day")
        .annotate(
            total_expenses=Sum(
                Case(
                    When(type_data="0", then="value"),
                    default=0,
                    output_field=FloatField(),
                )
            ),
            total_incomes=Sum(
                Case(
                    When(type_data="1", then="value"),
                    default=0,
                    output_field=FloatField(),
                )
            ),
        )
        .order_by("day")
    )

    labels = [entry["day"].strftime("%Y-%m-%d") for entry in daily_qs]
    expenses_data = [entry["total_expenses"] or 0 for entry in daily_qs]
    incomes_data = [entry["total_incomes"] or 0 for entry in daily_qs]

    # Get the Categories
    categories = Category.objects.filter(user=request.user)

    context = {
        "expenses": expenses,
        "categories": categories,
        "labels_json": json.dumps(labels),
        "expenses_json": json.dumps(expenses_data),
        "incomes_json": json.dumps(incomes_data),
        "form": form,
    }
    return render(request, "expenses/expenses.html", context)


@login_required
def see_all(request):
    # 1) Parse date range from GET params (if any)
    start_str = request.GET.get("start_date")
    end_str = request.GET.get("end_date")
    if start_str and end_str:
        start_date = datetime.datetime.strptime(start_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_str, "%Y-%m-%d").date()
    else:
        # default: full span of user's data
        agg = Expense.objects.filter(user=request.user).aggregate(
            min_date=Min("issue_date"),
            max_date=Max(
                "issue_date",
            ),
        )
        start_date = (
            agg["min_date"].date() if agg["min_date"] else timezone.now().date()
        )
        end_date = agg["max_date"].date() if agg["max_date"] else timezone.now().date()

    # 2) Filter and compute stats
    expenses = (
        Expense.objects.filter(
            user=request.user,
            issue_date__date__gte=start_date,
            issue_date__date__lte=end_date,
        )
        .prefetch_related("categories")
        .order_by("-issue_date", "-date_reg")
    )
    total_expenses = sum(e.value if e.type_data == "0" else 0 for e in expenses)
    total_income = sum(e.value if e.type_data == "1" else 0 for e in expenses)
    total = total_income - total_expenses
    average = total / len(expenses) if expenses else 0

    # 3) Daily aggregates for chart
    daily_qs = (
        expenses.annotate(day=TruncDate("issue_date"))
        .values("day")
        .annotate(
            total_expenses=Sum(
                Case(
                    When(type_data="0", then="value"),
                    default=0,
                    output_field=FloatField(),
                )
            ),
            total_incomes=Sum(
                Case(
                    When(type_data="1", then="value"),
                    default=0,
                    output_field=FloatField(),
                )
            ),
        )
        .order_by("day")
    )
    labels = [e["day"].strftime("%Y-%m-%d") for e in daily_qs]
    expenses_data = [e["total_expenses"] or 0 for e in daily_qs]
    incomes_data = [e["total_incomes"] or 0 for e in daily_qs]

    # 4) Build frequency dict for word cloud

    img_str = ""
    if len(expenses) > 0:
        freq_dict = {}
        for e in expenses:
            desc = e.description.capitalize().strip()
            freq_dict[desc] = freq_dict.get(desc, 0) + float(e.value)

        # Generate the word cloud image
        wc = WordCloud(
            width=800,
            height=400,
            background_color="white",
            max_words=100,
        ).generate_from_frequencies(freq_dict)

        # Convert image to base64
        buffer = BytesIO()
        wc.to_image().save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # 5) Agregar sumas de gastos por categoría
    category_stats = (
        expenses.values("categories__name")
        .annotate(
            total=Sum(
                Case(
                    When(type_data="0", then="value"),
                    default=0,
                    output_field=FloatField(),
                )
            )
        )
        .order_by("-total")
    )

    # Construimos listas JSON para usar en un gráfico si quieres
    cat_labels = [c["categories__name"] for c in category_stats]
    cat_values = [c["total"] for c in category_stats]

    context: dict = {
        "expenses": expenses,
        "total_expenses": f"${total_expenses:,.2f}",
        "total_income": f"${total_income:,.2f}",
        "total": f"${total:,.2f}",
        "average": f"${average:,.2f}",
        "labels_json": json.dumps(labels),
        "expenses_json": json.dumps(expenses_data),
        "incomes_json": json.dumps(incomes_data),
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "wordcloud_img": img_str,
        "category_stats": category_stats,
        "cat_labels": json.dumps(cat_labels),
        "cat_values": json.dumps(cat_values),
    }
    return render(request, "expenses/see_all.html", context)


@login_required
def download_data(request):
    "Download all expenses as CSV"
    if request.method != "POST":
        return redirect("see_all")
    expenses = Expense.objects.filter(user=request.user)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="expenses.csv"'
    writer = csv.writer(response)
    writer.writerow(["description", "value", "type_data", "date"])
    for e in expenses:
        writer.writerow([e.description, e.value, e.get_type_data_display(), e.date_reg])
    return response


@login_required
def delete_expense(request, expense_id):
    """Delete a single expense entry."""
    # Fetch the expense belonging to the current user or return 404
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == "POST":
        expense.delete()
        messages.success(request, "Expense deleted successfully.")
    else:
        messages.error(request, "Invalid request method.")

    return redirect("index")
