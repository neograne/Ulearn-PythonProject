from django.urls import path
from . import views

urlpatterns = [
    # Главная
    path('', views.home, name='home'),
    
    # Каталог
    path('cpu/', views.cpu_list, name='cpu_list'),
    path('cpu/<int:pk>/', views.cpu_detail, name='cpu_detail'),
    path('gpu/', views.gpu_list, name='gpu_list'),
    path('gpu/<int:pk>/', views.gpu_detail, name='gpu_detail'),
    path('motherboard/', views.motherboard_list, name='motherboard_list'),
    path('ram/', views.ram_list, name='ram_list'),
    path('psu/', views.psu_list, name='psu_list'),
    path('case/', views.case_list, name='case_list'),
    
    # Сборки
    path('builds/', views.build_list, name='build_list'),
    path('builds/<int:pk>/', views.build_detail, name='build_detail'),
    path('builds/new/', views.build_create, name='build_create'),
    path('builds/<int:pk>/edit/', views.build_edit, name='build_edit'),
    path('builds/<int:pk>/delete/', views.build_delete, name='build_delete'),
    path('my-builds/', views.my_builds, name='my_builds'),
    
    # Регистрация
    path('register/', views.register, name='register'),
]