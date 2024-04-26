from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_map, name='show_map'),
    path('add_farm/', views.add_farm, name='add_farm'),
    path('view_farms/', views.view_farms, name='view_farms'),

    # URL pattern for updating a farm
    path('update_farm/<int:farm_id>/', views.update_farm, name='update_farm'),

    # URL pattern for deleting a farm
    path('delete_farm/<int:farm_id>/', views.delete_farm, name='delete_farm'),
]
