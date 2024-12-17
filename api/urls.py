"""
URL configuration for webscraping_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path

from .views import scrape_data_detail_view, scrape_url_post_view, scrape_view, search_data_view

urlpatterns = [
    path('scrape/', scrape_url_post_view, name='scrape_url'),
    path('scraped_data/', scrape_view, name='scraped_data'),
    path('scraped_data/<int:pk>/', scrape_data_detail_view, name='scraped_data_detail'),
    path('search/', search_data_view, name='search_data')
    ]
