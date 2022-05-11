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
from django.contrib import admin
from django.urls import path, include

from . import views, api_views

admin.AdminSite.site_title = 'Radio Universe'
admin.AdminSite.site_header = 'Radio Universe Administration'
urlpatterns = [
    path('', api_views.index, name='index'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('countries', api_views.countries, name='countries'),
    path('continents', api_views.continents, name='continents'),
    path('<continent>/countries', api_views.get_countries, name='get-countries'),
    path('<country_code>/stations', api_views.get_stations, name='get-stations'),
    path('<country_code>/<int:page_number>', api_views.get_stations_by_page),
    path('<country_code>/save', api_views.save_to_db),
    path('save-all', api_views.save_all_to_db),
]
