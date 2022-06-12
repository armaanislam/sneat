from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class KpiConfigForm(ModelForm):
    class Meta:
        model = KPIConfig
        fields = '__all__'


class ReviewRatingForm(ModelForm):
    class Meta:
        model = ReviewRating
        fields = '__all__'


class SupervisorForm(ModelForm):
    class Meta:
        model = Supervisor
        fields = '__all__'