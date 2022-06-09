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
    group = models.CharField(max_length=50,blank=True, null=True )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date', '-updated_date']

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']



class Log(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    component = models.CharField(max_length=30)
    login_date = models.DateTimeField(null=True)
    logout_date = models.DateTimeField(null=True)
    date_time = models.DateTimeField()
    ip = models.GenericIPAddressField()

    class Meta:
        db_table = 'logger'



class ReviewRating(models.Model):
    name = models.CharField(max_length=255, null=True)
    rating = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_rating_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_rating_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name



class KPIConfig(models.Model):
    name = models.CharField(max_length=255)
    rating = models.ForeignKey(ReviewRating, on_delete=models.CASCADE)
    year = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name



class Supervisor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Project(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name



class SBU(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_sbu_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_sbu_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name



class SubSBU(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_sub_sbu_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_sub_sbu_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name



class KPIObjective(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_objective_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpi_objective_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name



class Employee(models.Model):
    name = models.CharField(max_length=255)
    employee_id = models.PositiveIntegerField(primary_key=True)
    designation = models.CharField(max_length=255, null=True)
    sbu = models.ForeignKey(SBU, on_delete=models.CASCADE, null=True)
    sub_sbu = models.ForeignKey(SubSBU, on_delete=models.CASCADE, null=True)
    date_of_joining = models.DateField(auto_now_add=True, null=True)
    basic_salary = models.FloatField(default=None, null=True)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_updated_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.name
