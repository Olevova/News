from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value):
    mat = ["дурак", 'невежда', 'редиска']
    c = value.split()
    for i in c:
        if i.lower() in mat:
            raise ValueError(f'Нельзя употреблять это слово {i}')
    else:
        return value


