from django import template
import textwrap

register = template.Library()



@register.filter
def tostr(value):
    return str(value)

@register.filter
def split_into_paragraphs(value, char_limit=250):
    # Split the value into paragraphs after every char_limit characters
    paragraphs = [value[i:i+char_limit] for i in range(0, len(value), char_limit)]
    return '\n'.join('<p>{}</p>'.format(p) for p in paragraphs)