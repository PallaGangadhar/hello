from django import template
from hello_world.models import category

register = template.Library()
@register.inclusion_tag('design/cats.html')
def get_category_list():
    return {'cats':category.objects.all()}

# def get_category_list1(cat1 = None):
#     return {'cats':category.objects.all(),'act_cat':cat1}