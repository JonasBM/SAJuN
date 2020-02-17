from django import template
register = template.Library()

@register.filter
def check_proprietario(objetos, user):
    return objetos.filter(proprietario=user)