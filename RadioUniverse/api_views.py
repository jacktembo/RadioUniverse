import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import RadioStation
from .utils import countries as all_countries, country_codes
from .utils import continents as all_continents, radio_base_url
from bs4 import BeautifulSoup
from threading import Thread

def calculate_pages(soup):
    return 1 if len(soup.select('.pagination')) < 1 else int(soup.select('.pagination')[0].contents[-4].text)


@api_view()
def countries(request):
    """Get all the countries available on the platform."""
    return Response(all_countries)


@api_view()
def continents(request):
    """get all the continents available on the platform."""
    return Response(all_continents)


@api_view()
def get_stations(request, country_code):
    """Get radio stations by just providing a country code."""
    url = radio_base_url + country_code
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    button_list = soup.select('.station_play')
    number_of_pages = calculate_pages(soup)
    data = [
        {
            'station_name': button['radioname'], 'url': button['stream'], 'stream_type': button['streamtype'],
            'radio_image': button['radioimg'], 'api_developer': 'Jack Tembo',
            'api_developer_website': 'https://jacktembo.com',
            'number_of_pages': number_of_pages
        } for button in button_list
    ]
    return Response(data)


@api_view()
def get_stations_by_page(request, country_code, page_number):
    url = radio_base_url + country_code + f'/?p={page_number}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    button_list = soup.select('.station_play')
    number_of_pages = calculate_pages(soup)
    data = [
        {
            'station_name': button['radioname'], 'url': button['stream'], 'stream_type': button['streamtype'],
            'radio_image': button['radioimg'], 'api_developer': 'Jack Tembo',
            'api_developer_website': 'https://jacktembo.com',
            'number_of_pages': number_of_pages
        } for button in button_list
    ]
    return Response(data)


@api_view()
def get_countries(request, continent):
    """Get countries and their respective codes by providing a continent name."""
    r = requests.get(radio_base_url + continent + '/')
    soup = BeautifulSoup(r.text, 'html.parser')
    countries = soup.select('.countries__countries-list')[0].find_all('li')

    countries_list = {str(country.a['href'][1:-1].upper()): str(country.string) for country in countries}
    return Response(countries_list)


@api_view()
def save_to_db(request, country_code):
    url = radio_base_url + country_code
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    button_list = soup.select('.station_play')
    number_of_pages = calculate_pages(soup)

    for page_number in range(number_of_pages):
        url = radio_base_url + country_code + f'/?p={page_number}'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        button_list = soup.select('.station_play')
        data = [
            {
                'station_name': button['radioname'], 'url': button['stream'], 'stream_type': button['streamtype'],
                'radio_image_url': button['radioimg'], 'api_developer': 'Jack Tembo',
                'api_developer_website': 'https://jacktembo.com',

            } for button in button_list
        ]
        for station in data:
            RadioStation.objects.create(name=station['station_name'], url=station['url'])

    return Response('Successfully Saved items.')


def save_all_to_db(request):
    try:
        for country_code in country_codes:
            save_thread = Thread(target=save_to_db(request, country_code))
            save_thread.start()
        return HttpResponse('countries saved')

    except Exception as e:
        return HttpResponse(e)


def index(request):
    return HttpResponse('Welcome To Radio Universe.')


@api_view()
def developer(request):
    api_developer = {
        'first_name': 'Jack', 'last_name': 'Tembo', 'email': 'jack@jacktembo.com',
        'website': 'https://www.jacktembo.com', 'nationality': 'Zambian', 'city': 'Lusaka',
        'developer_experience': '10 Years'
    }
    return Response(api_developer)

@api_view()
def search(request):
    query = request.GET.get('q', None)
    country_code = request.GET.get('c', None)
    style = request.GET.get('s', None)
    url = f'https://onlineradiobox.com/search?q={query}&c={country_code}&s={style}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    button_list = soup.select('.station_play')
    number_of_pages = calculate_pages(soup)
    data = [
        {
            'station_name': button['radioname'], 'url': button['stream'], 'stream_type': button['streamtype'],
            'radio_image': button['radioimg'], 'api_developer': 'Jack Tembo',
            'api_developer_website': 'https://jacktembo.com',
            'number_of_pages': number_of_pages
        } for button in button_list
    ]
    return Response(data)

