from django.contrib import admin
from django.urls import path
from salary_parser.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
]
