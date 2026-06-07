from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()

# Minimal currency symbol map. Anything not listed falls back to
# "<CODE> <amount>" (e.g. "MXN 1,234.50").
CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "COP": "$",
}


@register.filter
def currencyfmt(value, currency="USD"):
    """Format a number as currency, e.g. ``1234.5`` -> ``"$1,234.50"``.

    Drop-in replacement for the ``currencyfmt`` filter that django-babel used
    to provide, so the templates keep working without that (unmaintained)
    dependency. Negatives are rendered as ``-$5.00`` to match the old output.
    """
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return value

    symbol = CURRENCY_SYMBOLS.get(str(currency).upper())
    sign = "-" if amount < 0 else ""
    formatted = f"{abs(amount):,.2f}"

    if symbol:
        return f"{sign}{symbol}{formatted}"
    return f"{sign}{currency} {formatted}"
