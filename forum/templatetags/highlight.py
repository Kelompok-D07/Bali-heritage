from django import template
import re

register = template.Library()

@register.filter
def highlight(text, search):
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return pattern.sub(lambda m: '<span class="bg-yellow-200">{}</span>'.format(m.group()), text)
