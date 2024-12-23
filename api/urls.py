from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import UserViewSet, TaskViewSet,CatagoryViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
router = DefaultRouter()

# router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'users', UserViewSet, basename='user')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'catagories', CatagoryViewSet, basename='catagory')

urlpatterns = [ 
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
               ] 
urlpatterns += router.urls