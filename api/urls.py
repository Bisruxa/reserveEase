from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import UserViewSet, TaskViewSet,UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView
router = DefaultRouter()


router.register(r'auth/register', UserViewSet, basename='users')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'users/me', UserProfileView, basename='me')

urlpatterns = [ 
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
   ] 
urlpatterns += router.urls