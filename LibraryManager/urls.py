"""LibraryManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from management import views as management_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^add_author/$', management_views.add_author),
    url(r'^show_authors/$', management_views.show_authors),
    url(r'^add_book/$', management_views.add_book),
    url(r'^show_book/$', management_views.show_book),
    url(r'^show_book_detail/$', management_views.show_book_detail),
    url(r'^show_author_detail/$', management_views.show_author_detail),
    url(r'^change_author_detail/$', management_views.change_author_detail),
    url(r'^change_book_detail/$', management_views.change_book_detail),
    url(r'^$', management_views.index),
]















