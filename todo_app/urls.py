from django.urls import path
from . import views

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )


urlpatterns = [
    # path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('tasks/', views.TodoListViewAll.as_view()),
    path('tasks/<str:pk>/', views.TodoSingleView.as_view()),
    path('register/', views.Register.as_view()),
    path('login/', views.Login.as_view()),


    path('',views.home, name = 'home'),
    path('home2/', views.home2, name = 'home2')
    
   
]


