"""
URL Routes for User API
"""

from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('/create/', views.CreateUserView.as_view(), name='create'),
    path('/token/', views.CreateAuthTokenView.as_view(), name='token'),
    path('/manage_user', views.ManageUserView.as_view(), name='manage_user'),
    path('/user_profile', views.UserProfileView.as_view(), name='user_profile')
]