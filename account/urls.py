from django.urls import path

from . import views

urlpatterns = [
    path('', views.TransactionList.as_view(), name='transaction_list'),
    path('<int:pk>/', views.TransactionDetail.as_view(), name='transaction_detail'),
    path('create/', views.TransactionCreate.as_view()),
    path('update/<int:pk>/', views.TransactionUpdate.as_view(), name='transaction_update'),
    path('delete/<int:pk>/', views.TransactionDelete.as_view(), name='transaction_delete'),
]