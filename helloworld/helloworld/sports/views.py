from django.shortcuts import render

def sport(request):
    return render(request, 'home.html', {'title': 'Главная', 'message': 'Добро пожаловать на сайт о спорте!'})

def football(request):
    return render(request, 'football.html', {'title': 'Футбол', 'message': 'Раздел о футболе'})

def hockey(request):
    return render(request, 'hockey.html', {'title': 'Хоккей', 'message': 'Раздел о хоккее'})

def basketball(request):
    return render(request, 'basketball.html', {'title': 'Баскетбол', 'message': 'Раздел о баскетболе'})


