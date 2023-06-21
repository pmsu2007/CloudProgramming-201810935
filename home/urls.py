from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.GoalList.as_view(), name='goal_list'),
    path('login/', auth_views.LoginView.as_view(template_name='home/loginPage.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('goal/create/', views.GoalCreate.as_view(), name='goal_create'),
    path('goal/<int:pk>/', views.GoalDetail.as_view(), name='goal_detail'),
    path('goal/update/<int:pk>/', views.GoalUpdate.as_view(), name='goal_update'),
    path('goal/delete/<int:pk>/', views.GoalDelete.as_view(), name='goal_delete')
]