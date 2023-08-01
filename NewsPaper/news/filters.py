import django_filters
from django_filters import FilterSet, ChoiceFilter, CharFilter, DateFromToRangeFilter, NumberFilter
from .models import Post


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок',
    )
    author_user_username = CharFilter(
        field_name='author__user__username',
        lookup_expr='exact',
        label='Имя автора'
    )
    rating = NumberFilter(
        field_name='rating',
        lookup_expr='gte',
        label='Рейтинг от'
    )
    date_time = DateFromToRangeFilter(
        field_name='date_time',
        lookup_expr='gte',
        label='Дата',
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'})
    )
    post_type = ChoiceFilter(
        field_name='post_type',
        label='Тип поста',
        empty_label='Любой',
        choices=Post.POST_TYPE_CHOICES
    )


