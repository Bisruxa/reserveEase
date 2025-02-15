from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import UserViewSet, TaskViewSet, TableViewSet
from .views import SigninView


router = DefaultRouter()

 
router.register(r'auth/register', UserViewSet, basename='users')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'tables', TableViewSet, basename='table')







# Define the URL patterns
urlpatterns = [

    path('auth/signin/', SigninView.as_view(), name='signin'), 
 
]

# Add the router-generated URLs
urlpatterns += router.urls
