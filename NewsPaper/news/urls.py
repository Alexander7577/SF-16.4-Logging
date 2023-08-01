from django.urls import path
from django.views.decorators.cache import cache_page
from .views import NewsList, PieceOfNewsDetail, NewsListSearch, NewsCreate, NewsUpdate, NewsDelete, AuthorGroup, \
   upgrade_me, CategoryList, subscribe


urlpatterns = [
   path('', NewsList.as_view(), name='news_list'),
   path('search', NewsListSearch.as_view(), name='search_list'),
   path('<int:pk>', PieceOfNewsDetail.as_view(), name='Piece_Of_News_Detail'),
   path('create', NewsCreate.as_view(), name='create_news'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='update_news'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='delete_news'),
   path('author', AuthorGroup.as_view(), name='authorgroup'),
   path('author/upgrade', upgrade_me, name='upgrade'),
   path('categories/<int:pk>', CategoryList.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]