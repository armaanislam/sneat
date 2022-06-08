from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=255)
    forget_password_token = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    organization = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    zipcode = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']



class KPIConfig(models.Model):
    name = models.CharField(max_length=255)
    rating = models.ForeignKey('ReviewRating', on_delete=models.CASCADE)
    year = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name



class ReviewRating(models.Model):
    RATINGS = (
        ("1. Exceeded.", "1. Exceeded."),
        ("2. Achieved all aspects.", "2. Achieved all aspects."),
        ("3. Achieved the essnential requirements.", "3. Achieved the essnential requirements."),
        ("4. Did not achieve.", "4. Did not achieve."),
    )
    rating = models.CharField(max_length=255, blank=True, default='', choices=RATINGS)

    def __str__(self):
        return self.rating



class Employee(models.Model):
    name = models.CharField(max_length=255)
    employee_id = models.PositiveIntegerField(primary_key=True)
    designation = models.CharField(max_length=255, null=True)
    sbu = models.ForeignKey('SBU', on_delete=models.CASCADE, null=True)
    sub_sbu = models.ForeignKey('SubSBU', on_delete=models.CASCADE, null=True)
    date_of_joining = models.DateTimeField(auto_now_add=True, null=True)
    basic_salary = models.FloatField(default=None, null=True)

    def __str__(self):
        return self.name



class Project(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class SBU(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class SubSBU(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class KPIObjective(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name