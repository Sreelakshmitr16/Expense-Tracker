from django import forms
from budget.models import Transaction
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        # fields='__all__'
        exclude=("created_date","user_object",) #exclude should be given in tuple format :if only one field ,then should be given as:("a",)
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control',"placeholder":'enter title'}),
            'amount':forms.NumberInput(attrs={'class':'form-control',"amount":"enter amount"}),
            'type':forms.Select(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            }
        
class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control' ,"placeholder":"enter password"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control',"placeholder":"confirm password"}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'})
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))


    