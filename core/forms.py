from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Family

class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    family_name = forms.CharField(max_length=100, required=False)
    join_family_code = forms.CharField(max_length=20, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Создать новую семью или присоединиться
        if self.cleaned_data.get('family_name'):
            family = Family.objects.create(name=self.cleaned_data['family_name'])
            user.family = family
        
        if commit:
            user.save()
        return user