from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=255, unique=False, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Required fields for creating a superuser
    objects = UserManager()
    

    def __str__(self):
        return self.email

class Catagory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):  
        return self.name
class Task(models.Model):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]  
    
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]
    

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    catagory = models.ForeignKey(Catagory, on_delete=models.SET_NULL, null=True,blank = True , related_name = 'tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()  # Default as a function
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default=LOW)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return self.title

    def clean(self):  # Validate that the due_date is in the future
        if timezone.is_naive(self.due_date):
            self.due_date = timezone.make_aware(self.due_date, timezone.get_current_timezone())

        if self.due_date <= timezone.now():
            raise ValidationError("Due date must be in the future")

    def save(self, *args, **kwargs):
        self.clean()  # Ensure clean validation is called before saving
        super().save(*args, **kwargs)

    def set_status(self, new_status):
        if self.status == self.COMPLETED and new_status != self.COMPLETED:
            raise ValidationError("Completed tasks cannot be changed to another status.")
        self.status = new_status
        self.save()
