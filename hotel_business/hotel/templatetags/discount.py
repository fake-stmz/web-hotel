from django import template

register = template.Library()

@register.filter
def discount(value, request):
    return (value - (value * request.user.guest_info.discount / 100))