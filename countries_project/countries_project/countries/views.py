import requests
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .forms import LanguageForm


def country_list(request):
    url = 'https://restcountries.com/v3.1/all'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Если data - список, используем его, иначе пустой список
        if isinstance(data, list):
            countries = data
        else:
            countries = []

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        countries = []

    return render(request, 'countries/country_list.html', {'countries': countries})
def country_detail(request, country_name):
    response = requests.get(f'https://restcountries.com/v3.1/name/{country_name}')
    country = response.json()[0]  # Получаем первый элемент списка
    return render(request, 'countries/country_detail.html', {'country': country})


def region_list(request):
    response = requests.get('https://restcountries.com/v3.1/all')
    countries = response.json()

    # Создаем множество регионов для избежания дублирования
    regions = {country['region'] for country in countries if country['region']}
    return render(request, 'countries/region_list.html', {'regions': regions})


def region_detail(request, region_name):
    response = requests.get(f'https://restcountries.com/v3.1/region/{region_name}')
    region_countries = response.json()
    return render(request, 'countries/region_detail.html', {'region_name': region_name, 'countries': region_countries})

def city_detail(request, city_name):
    response = requests.get(f'https://restcountries.com/v3.1/capital/{city_name}')
    city_info = response.json()[0]  # Получаем первую запись из ответа
    return render(request, 'countries/city_detail.html', {'city_info': city_info})


def language_search(request):
    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            language = form.cleaned_data['language']
            response = requests.get(f'https://restcountries.com/v3.1/lang/{language}')
            countries = response.json()
            return render(request, 'countries/language_results.html', {'countries': countries, 'language': language})
    else:
        form = LanguageForm()

    return render(request, 'countries/language_search.html', {'form': form})
