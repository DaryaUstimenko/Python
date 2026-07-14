from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Book, Reader

admin.site.register(Book)
admin.site.register(Reader)
# Создаем группу "Читатели" и добавляем разрешение на просмотр книг
def create_readers_group():
    readers_group, created = Group.objects.get_or_create(name='Читатели')
    content_type = ContentType.objects.get_for_model(Book)
    permission = Permission.objects.get(
        codename='view_book',
        content_type=content_type,
    )
    readers_group.permissions.add(permission)

# Проверяем, существует ли группа "Читатели", и создаем ее при необходимости
create_readers_group()

