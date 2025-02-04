from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import UserViewSet, TaskViewSet, TableViewSet,ReservationViewSet  
from rest_framework_simplejwt.views import TokenObtainPairView


router = DefaultRouter()


router.register(r'auth/register', UserViewSet, basename='users')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'tables', TableViewSet, basename='table')
router.register(r'reservations',ReservationViewSet) 

# Define the URL patterns
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
]

# Add the router-generated URLs
urlpatterns += router.urls
