from datetime import datetime
from firebase_admin import firestore


class Expense():
    def __init__(self, description, value, type_data, user, date_reg=None):
        self.description = description
        self.value = float(value)
        self.type_data = type_data
        self.user = user

        if date_reg is None:
            self.date_reg = datetime.now()
        else:
            self.date_reg = date_reg

        self.date_string = self.date_reg.strftime("%d-%m-%Y %H:%M:%S")

    def saveExpense(self):
        db = firestore.client()
        db.collection("expenses").document().set(self.__dict__)

    @staticmethod
    def generateCsv(expenses, separator=";"):
        csv = f"description{separator}value{separator}type{separator}date\n"
        for expense in expenses:
            csv += f"{expense.description}{separator}{expense.value}{separator}{expense.type_data}{separator}{expense.date_string}\n"
        return csv

    @staticmethod
    def sumOfExpenses(expenses):
        sum = 0
        for expense in expenses:
            if expense.type_data == "0":
                sum -= expense.value
            else:
                sum += expense.value

        return sum

    @staticmethod
    def averageOfExpenses(expenses):
        return Expense.sumOfExpenses(expenses) / len(expenses)

    @staticmethod
    def getExpenses(user=None, limit=20, order="desc"):
        db = firestore.client()
        db_ref = db.collection("expenses")
        if user is not None:
            db_ref = db_ref.where(u'user', u'==', user)

        if order == "desc":
            db_ref = db_ref.order_by(
                'date_reg', direction=firestore.Query.DESCENDING)
        else:
            db_ref = db_ref.order_by(
                'date_reg', direction=firestore.Query.ASCENDING)

        if limit is not None:
            db_ref = db_ref.limit(limit)

        db_ref = db_ref.get()

        data = []

        for i in db_ref:
            i = i.to_dict()
            description = i.get("description", "")
            user = i.get("user", "")
            value = i.get("value", "")
            type_data = i.get("type_data", "")
            date_reg = i.get("date_reg", "")

            data.append(Expense(description, value, type_data, user, date_reg))

        return data
