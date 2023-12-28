from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
import requests
import pandas as pd
from .models import EmployeeSalary, SalaryData

def get_city_id(city_name):
    """Получение ID города из API hh.ru."""
    url = "https://api.hh.ru/areas"
    response = requests.get(url)
    if response.status_code == 200:
        areas = response.json()
        for country in areas:
            if country['name'].lower() == city_name.lower():
                return country['id']
            for region in country['areas']:
                if region['name'].lower() == city_name.lower():
                    return region['id']
                for city in region['areas']:
                    if city['name'].lower() == city_name.lower():
                        return city['id']
    return None

def parse_vacancies():
    """Парсинг зарплат по вакансиям 'Продавец-Консультант' в каждом городе"""
    cities = EmployeeSalary.objects.values_list('city', flat=True).distinct()
    for city_name in cities:
        city_id = get_city_id(city_name)
        if city_id is None:
            print(f"Город {city_name} не найден в API.")
            continue

        # Определение параметров запроса
        params = {
            "text": "Продавец-Консультант",
            "area": city_id,
            "per_page": 100  # Максимальное количество результатов на странице
        }
        headers = {"User-Agent": "parser/1.0 (anyemail@anyclient.com)"}

        # Отправка запроса
        response = requests.get("https://api.hh.ru/vacancies", params=params, headers=headers)
        if response.status_code == 200:
            vacancies = response.json().get("items", [])
            total_salary = 0
            count = 0

            # Сбор данных о зарплатах
            for vacancy in vacancies:
                salary = vacancy.get("salary")
                if salary and salary.get("from"):
                    total_salary += salary.get("from")
                    count += 1

            if count > 0:
                average_salary = total_salary / count
                SalaryData.objects.update_or_create(city=city_name, defaults={'salary': average_salary})
                print(f"Данные по городу {city_name} обновлены.")
        else:
            print(f"Ошибка запроса для города {city_name}: {response.status_code}")

@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == 'POST':
        parse_vacancies()  # Запуск парсинга
        return redirect('index')  # Перезагрузка страницы после парсинга

    # Получение данных для отображения
    employee_salaries = EmployeeSalary.objects.all()
    market_salaries = SalaryData.objects.all()
    context = {
        'employee_salaries': employee_salaries,
        'market_salaries': market_salaries
    }
    return render(request, 'index.html', context)