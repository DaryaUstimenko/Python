from django.contrib import admin
from .models import Article, Tag, SavedArticle, Comment

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date', 'is_public')
    list_filter = ('is_public', 'tags', 'author')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
# filter_horizontal заменяет его на два списка: «Доступные теги» и «Выбранные теги» с кнопками перемещен#ия между ними. Это особенно полезно, когда тегов много.
@admin.register(SavedArticle)
class SavedArticleAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'saved_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'created_at')

