from django import template


register = template.Library()


@register.filter(name='get_dynamic_attribute')
def get_dynamic_attribute(obj, attr_name):
    return getattr(obj, attr_name, '')
