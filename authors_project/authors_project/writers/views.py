from django.shortcuts import render, redirect

WRITERS_DATA = [
    {
        'slug': 'hemingway',
        'name': 'Эрнест Хемингуэй',
        'full_name': 'Эрнест Миллер Хемингуэй',
        'birth_year': 1899,
        'death_year': 1961,
        'country': 'США',
        'biography': 'Американский писатель, журналист, лауреат Нобелевской премии по литературе (1954). Известен своим лаконичным и суровым стилем письма.',
        'famous_works': ['Старик и море', 'По ком звонит колокол', 'Прощай, оружие!', 'Фиеста (И восходит солнце)'],
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/e/e6/Ernest_Hemingway_1950.jpg'
    },
    {
        'slug': 'shakespeare',
        'name': 'Уильям Шекспир',
        'full_name': 'Уильям Шекспир',
        'birth_year': 1564,
        'death_year': 1616,
        'country': 'Англия',
        'biography': 'Английский поэт и драматург, считается величайшим писателем на английском языке и одним из лучших драматургов мира.',
        'famous_works': ['Гамлет', 'Ромео и Джульетта', 'Отелло', 'Король Лир', 'Макбет'],
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/a/a2/Shakespeare.jpg'
    },
    {
        'slug': 'tolstoy',
        'name': 'Лев Толстой',
        'full_name': 'Лев Николаевич Толстой',
        'birth_year': 1828,
        'death_year': 1910,
        'country': 'Россия',
        'biography': 'Один из наиболее известных русских писателей и мыслителей, один из величайших писателей-романистов мира.',
        'famous_works': ['Война и мир', 'Анна Каренина', 'Воскресение', 'Смерть Ивана Ильича'],
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/5/5a/Lev_Tolstoy_1897.jpg'
    },
    {
        'slug': 'dostoevsky',
        'name': 'Фёдор Достоевский',
        'full_name': 'Фёдор Михайлович Достоевский',
        'birth_year': 1821,
        'death_year': 1881,
        'country': 'Россия',
        'biography': 'Русский писатель, мыслитель, философ и публицист. Классик мировой литературы.',
        'famous_works': ['Преступление и наказание', 'Идиот', 'Братья Карамазовы', 'Бесы'],
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/7/7f/Dostoevsky_1872.jpg'
    },
    {
        'slug': 'austen',
        'name': 'Джейн Остин',
        'full_name': 'Джейн Остин',
        'birth_year': 1775,
        'death_year': 1817,
        'country': 'Великобритания',
        'biography': 'Английская писательница, автор романов о жизни английского дворянства.',
        'famous_works': ['Гордость и предубеждение', 'Разум и чувства', 'Эмма', 'Мэнсфилд-парк'],
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/c/cb/Jane_Austen_1870_portrait.jpg'
    },
    {
        'slug': 'marquez',
        'name': 'Габриэль Гарсиа Маркес',
        'full_name': 'Габриэль Гарсиа Маркес',
        'birth_year': 1927,
        'death_year': 2014,
        'country': 'Колумбия',
        'biography': 'Колумбийский писатель, журналист, лауреат Нобелевской премии по литературе (1982). Представитель магического реализма.',
        'famous_works': ['Сто лет одиночества', 'Любовь во время холеры', 'Полковнику никто не пишет',
                         'Осень патриарха'],
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2f/Gabriel_Garcia_Marquez.jpg'
    }
]

BOOKS_DATA = [
    {'title': 'Война и мир', 'author_slug': 'tolstoy', 'author': 'Лев Толстой', 'rating': 9.8, 'year': 1869},
    {'title': 'Преступление и наказание', 'author_slug': 'dostoevsky', 'author': 'Фёдор Достоевский', 'rating': 9.7,
     'year': 1866},
    {'title': 'Анна Каренина', 'author_slug': 'tolstoy', 'author': 'Лев Толстой', 'rating': 9.6, 'year': 1877},
    {'title': 'Гордость и предубеждение', 'author_slug': 'austen', 'author': 'Джейн Остин', 'rating': 9.5,
     'year': 1813},
    {'title': 'Сто лет одиночества', 'author_slug': 'marquez', 'author': 'Габриэль Гарсиа Маркес', 'rating': 9.4,
     'year': 1982},
    {'title': 'Старик и море', 'author_slug': 'hemingway', 'author': 'Эрнест Хемингуэй', 'rating': 9.3, 'year': 1952},
    {'title': 'Гамлет', 'author_slug': 'shakespeare', 'author': 'Уильям Шекспир', 'rating': 9.9, 'year': 1603},
    {'title': 'Идиот', 'author_slug': 'dostoevsky', 'author': 'Фёдор Достоевский', 'rating': 9.2, 'year': 1869},
]

WRITERS_BY_SLUG = {writer['slug']: writer for writer in WRITERS_DATA}


def home(request):
    context = {
        'title': 'Главная',
        'welcome_message': 'Добро пожаловать в наше книжное приложение!',
        'writers_count': len(WRITERS_DATA),
        'books_count': len(BOOKS_DATA),
    }
    return render(request, 'home.html', context)


def writers(request):
    context = {
        'title': 'Писатели',
        'writers': WRITERS_DATA,
    }
    return render(request, 'writers.html', context)


def writer_detail(request, writer_slug):

    writer = WRITERS_BY_SLUG.get(writer_slug)

    if not writer:
        return redirect('writers')


    writer_books = [book for book in BOOKS_DATA if book.get('author_slug') == writer_slug]

    context = {
        'title': writer['name'],
        'writer': writer,
        'writer_books': writer_books,
    }
    return render(request, 'writer_detail.html', context)


def books(request):
    context = {
        'title': 'Топ лучших книг',
        'books': BOOKS_DATA,
    }
    return render(request, 'books.html', context)