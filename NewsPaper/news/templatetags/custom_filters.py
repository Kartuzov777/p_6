from django import template
import re

register = template.Library()

BAD_WORDS = ['редиска', 'дурак', 'глупец']


@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Фильтр 'censor' может применяться только к строкам.")

    for word in BAD_WORDS:
        pattern = rf'\b{word[0]}[а-яa-zё]*\b'  # используем raw string и f-строку
        replacement = word[0] + '*' * (len(word) - 1)
        value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)
    return value

@register.filter(name='in_group')
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()