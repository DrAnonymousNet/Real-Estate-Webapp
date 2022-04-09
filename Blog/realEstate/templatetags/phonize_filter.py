from django import template

register = template.Library()


def phonize(value):
    value = str(value)

    if value.startswith("0"):
        value = "+234 " + value[1:]
    elif value.startswith("234"):
        value = "+" + value
    elif value.startswith("8"):
        value = "+234 " + value
    return value

register.filter("phonize", phonize)