from django.urls import path

from .views import *

urlpatterns = [
    path('', homePageView, name='home'),
    path('problems', problemListView, name='problems'),
    path('problemjson', problemAsJsonView, name='problemJson'),
    path('hello', helloView, name='hello'),
]
