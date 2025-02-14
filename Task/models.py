from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not name:
            raise ValueError('User must have a name')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.is_active = True 
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None 
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Required fields for creating a superuser

    objects = UserManager()
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = None

    def save(self, *args, **kwargs):
        if self.password is not None and not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email



class Table(models.Model):
    table_id = models.AutoField(primary_key=True) 
    capacity = models.IntegerField()  
    availability = models.BooleanField(default=True)  
    status = models.CharField(max_length=50, choices=[('Available', 'Available'), ('Reserved', 'Reserved')], default='Available')

    def __str__(self):
        return f"Table {self.table_id} (Capacity: {self.capacity}) - {self.status}"


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
    table = models.ForeignKey(Table, on_delete=models.CASCADE, default=1)
    size = models.CharField(max_length=6, choices=SIZE_CHOICES, default=SMALL)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reservation_date = models.DateTimeField()  # Default as a function
    
    

    def __str__(self):
        return f"Reservation for {self.user.email} on {self.reservation_date}"

    def clean(self):  # Validate that the due_date is in the future and no existing reservation
        existing_reservation = Task.objects.filter(
            reservation_date=self.reservation_date,
            size=self.size
        ).exclude(id=self.id)
        
        if existing_reservation.exists():
            raise ValidationError("This reservation conflicts with an existing reservation.")

        if self.reservation_date <= timezone.now():
            raise ValidationError("Reservation date must be in the future.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
class Reservation(models.Model):
    customer_name = models.CharField(max_length=255)
    reservation_date = models.DateTimeField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL,null=True)
    status = models.CharField(max_length=50,default='Available')

    def __str__(self):
        return f"reservation fro {self.customer_name} on {self.reservation_date}"

