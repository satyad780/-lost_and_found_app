from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('upload/', views.upload_item, name='upload_item'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('test-csp/', views.test_csp, name='test_csp'),
]