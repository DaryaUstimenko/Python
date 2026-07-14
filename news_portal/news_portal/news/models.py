from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    publication_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)
    is_public = models.BooleanField(default=True, help_text="Доступна ли статья всем (True) или только авторизованным (False)")
    class Meta:
        ordering = ['-publication_date']  # по умолчанию новые сверху

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])

class SavedArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_articles')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'article')
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.article}'
