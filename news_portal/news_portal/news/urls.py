from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('article/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('article/<slug:slug>/save/', views.save_article, name='save_article'),
    path('article/<slug:slug>/unsave/', views.unsave_article, name='unsave_article'),
    path('saved/', views.saved_articles_list, name='saved_articles'),
]
