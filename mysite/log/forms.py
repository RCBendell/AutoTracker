from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import car, entry
from django.forms import ModelForm

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid Email Address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class CarCreationForm(forms.ModelForm):
    owner = forms.CharField(max_length=20, widget=forms.HiddenInput(), required=False)
    make = forms.CharField(max_length=30, required = True)
    model = forms.CharField(max_length=30, required = True)
    year = forms.IntegerField(min_value = 1900, required = True)
    color = forms.CharField(max_length = 15, required = False)
    mileage = forms.IntegerField(min_value=1, required = True)
    vin = forms.CharField(max_length = 30, required = False)

    class Meta:
        model = car
        fields = ('owner', 'make', 'model', 'year', 'color', 'vin', 'mileage',)

    

class LogEntryForm(forms.ModelForm):
    owner = forms.CharField(max_length=20, widget=forms.HiddenInput(), required=False)
    # This needs to be a drop down with all available users cars
    # car = forms.CharField()


    blog = forms.CharField(widget=forms.Textarea)
    cost = forms.DecimalField(decimal_places=2, required=False)

    #warranty = forms.BooleanField(default=False)

    class Meta:
        model = entry
        fields = ('owner', 'car', 'blog', 'cost',)

    def __init__(self, user, *args, **kwargs):
        super(LogEntryForm, self).__init__(*args, **kwargs)
        self.fields['car'].queryset = car.objects.filter(owner=user.get_username())
        