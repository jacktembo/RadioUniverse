"""RadioUniverse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from datetime import date, datetime, timedelta, time
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views, api_views

right_now = datetime.now()
hour = right_now.hour


def message():
    """
    Greeting message to be shown on the Admin Panel.
    :return:
    """
    return 'Good Morning' if 0 <= hour <= 11 else 'Good Day' if hour == 12 or hour == 13 else 'Good afternoon' if 13 <= hour <= 17 else 'Good Evening'


admin.AdminSite.site_title = 'Radio Universe'
admin.AdminSite.site_header = 'Radio Universe Administration'
admin.AdminSite.index_title = f'{message()} From Jack Tembo! How Are You Today? Welcome To The World\'s Largest ' \
                              f'Online Radio API. '

urlpatterns = [
    path('', api_views.index, name='index'),
    path('auth', include('djoser.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('world/countries', api_views.countries, name='countries'),
    path('world/continents', api_views.continents, name='continents'),
    path('<continent>/countries', api_views.get_countries, name='get-countries'),
    path('<country_code>/stations', api_views.get_stations, name='get-stations'),
    path('<country_code>/stations/<int:page_number>', api_views.get_stations_by_page),
    path('<country_code>/dump', api_views.save_to_db),
    path('world/dump', api_views.save_all_to_db),
    path('developer', api_views.developer, name='developer'),
    path(r'search', api_views.search, name='search'), # search whole world.
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
