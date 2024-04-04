from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', views.item_list, name='item_list'),
    path('item/create/', views.create_item, name='create_item'),
    path('item/edit/<int:pk>/', views.edit_item, name='edit_item'),
    path('item/delete/<int:pk>/', views.delete_item, name='delete_item'),
    path('bill/generate/', views.generate_bill, name='generate_bill'),
]
