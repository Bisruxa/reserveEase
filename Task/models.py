from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, email, password=None,username = None):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        user.is_active = True 
        return user

    def create_superuser(self, email, password=None,username = None):
        user = self.create_user(email, password,username)
        user.is_superuser = True
        user.is_staff = True
        
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=255, unique=False, blank=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Required fields for creating a superuser
    objects = UserManager()
    

    def __str__(self):
        return self.email

class Task(models.Model):
    SMALL = 'Small'
    MEDIUM = 'Medium'
    LARGE = 'Large'
    SIZE_CHOICES = [
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
    ]
    

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.CharField(max_length=6, choices=SIZE_CHOICES, default=SMALL)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reservation_date = models.DateTimeField()  # Default as a function
    
    

    def __str__(self):
        return f"Reservation for {self.user.email} on {self.date}"

    def clean(self):  # Validate that the due_date is in the future
        existing_reservation = Task.objects.filter(
            reservation_date=self.reservation_date,
            size=self.size
        ).exclude(id=self.id)
        
        if existing_reservation.exists():
            raise ValidationError("This reservation conflicts with an existing reservation.")

        if self.reservation_date <= timezone.now():
            raise ValidationError("Reservation date must be in the future.")


    def save(self, *args, **kwargs):
        self.clean()  # Ensure clean validation is called before saving
        super().save(*args, **kwargs)

