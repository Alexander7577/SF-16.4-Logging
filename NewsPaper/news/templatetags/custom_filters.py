from django import template

register = template.Library()


@register.filter()
def censor(text: str):
    ban_words = ['пизд', 'хуй', 'сука', 'ебал', 'твар', 'мраз', 'ёбан', 'мудак', 'гнид', 'пезд', 'хули', 'хуе',
                 'пидор', 'пидр', 'педик', 'шлюх', 'гандон', 'ебан', 'блядь']

    words = text.split()
    filtered_words = []
    for word in words:
        for ban_word in ban_words:
            if ban_word in word.lower():
                word = '*' * len(word)
                break
        filtered_words.append(word)
    filtered_text = ' '.join(filtered_words)
    return filtered_text

