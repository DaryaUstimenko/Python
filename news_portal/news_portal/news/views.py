from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Article, Tag, SavedArticle, Comment
from .forms import CommentForm


class ArticleListView(ListView):
    model = Article
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10  # Пагинатор подключается автоматически, если в ListView задан атрибут paginate_by

    # (или переопределён метод get_paginate_by). никаких дополнительных действий не требуется.

    def get_queryset(self):
        queryset = Article.objects.all()
        # Скрываем статьи для неавторизованных пользователей, если is_public=False
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_public=True)

        # Поиск по словам
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(text__icontains=q)
            )

        # Сортировка
        sort = self.request.GET.get('sort')
        if sort == 'date_asc':
            queryset = queryset.order_by('publication_date')
        elif sort == 'date_desc':
            queryset = queryset.order_by('-publication_date')
        elif sort == 'author':
            queryset = queryset.order_by('author__username')

        # Фильтр по тегу
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            try:
                tag = Tag.objects.get(slug=tag_slug)
                queryset = queryset.filter(tags=tag)
                self.selected_tag = tag  # сохраним для контекста
            except Tag.DoesNotExist:
                pass  # игнорируем неверный тег

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Все теги для фильтрации (выпадающий список)
        context['all_tags'] = Tag.objects.all()
        # Текущий выбранный тег
        context['selected_tag'] = getattr(self, 'selected_tag', None)

        # Текущие параметры для сохранения в шаблоне
        context['current_sort'] = self.request.GET.get('sort', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

    def dispatch(self, request, *args, **kwargs):
        # Проверяем доступ: если статья не публичная и пользователь не авторизован
        article = self.get_object()
        if not article.is_public and not request.user.is_authenticated:
            return redirect('login')  # перенаправляем на страницу входа
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all().order_by('-created_at')
        if self.request.user.is_authenticated:
            context['saved'] = SavedArticle.objects.filter(
                user=self.request.user, article=self.object
            ).exists()
        return context

@login_required
def add_comment(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
    return redirect('article_detail', slug=slug)

@login_required
def save_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    SavedArticle.objects.get_or_create(user=request.user, article=article)
    return redirect('article_detail', slug=slug)

@login_required
def unsave_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    SavedArticle.objects.filter(user=request.user, article=article).delete()
    return redirect('article_detail', slug=slug)

@login_required
def saved_articles_list(request):
    saved = SavedArticle.objects.filter(user=request.user).select_related('article')
    return render(request, 'news/saved_articles.html', {'saved_articles': saved})
