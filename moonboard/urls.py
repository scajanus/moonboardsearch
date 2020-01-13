from django.urls import path

from .views import homePageView, problemView, problemAsJsonView

urlpatterns = [
    path('', homePageView, name='home'),
    path('problems', problemView, name='problems'),
    path('problemjson', problemAsJsonView, name='problemJson'),

]