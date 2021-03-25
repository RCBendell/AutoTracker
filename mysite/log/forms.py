from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import car, entry, reminder
from django.forms import ModelForm
from bootstrap_datepicker_plus import DatePickerInput

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

    is_inspected = forms.BooleanField()
    inspected_exp = forms.DateField(required=False, help_text="For All Dates: use 'YYYY-MM-DD' Format")

    is_registered = forms.BooleanField()
    registered_exp = forms.DateField(required=False)

    is_insured = forms.BooleanField()
    insured_exp = forms.DateField(required=False)

    #Enable Reminders? Bool Field...

    class Meta:
        model = car
        fields = ('owner', 'make', 'model', 'year', 'color', 'vin', 'mileage', 'is_inspected', 'inspected_exp', 'is_registered', 'registered_exp', 'is_insured', 'insured_exp')

    

class LogEntryForm(forms.ModelForm):
    owner = forms.CharField(max_length=20, widget=forms.HiddenInput(), required=False)
    # This needs to be a drop down with all available users cars
    # car = forms.CharField()


    blog = forms.CharField(widget=forms.Textarea)
    cost = forms.DecimalField(decimal_places=2, required=False)

    date = forms.DateField(help_text="For All Dates: use 'YYYY-MM-DD' Format")

    #update_mileage = forms.PositiveIntegerField(required = True)

    #warranty = forms.BooleanField(default=False)

    class Meta:
        model = entry
        fields = ('owner', 'car', 'blog', 'cost','date')

    def __init__(self, user, *args, **kwargs):
        super(LogEntryForm, self).__init__(*args, **kwargs)
        self.fields['car'].queryset = car.objects.filter(owner=user.get_username())


class reminderForm(forms.ModelForm):
    owner = forms.CharField(max_length=20, widget=forms.HiddenInput(), required=False)
    email = forms.EmailField(widget=forms.HiddenInput(), required=False)
    msg = forms.CharField(widget=forms.Textarea)
    #remind_on_date = forms.DateField(
    #        widget=DatePickerInput(
    #            options={
    #                "format": "mm/dd/yyyy",
    #                "autoclose": True
    #            }
    #        )
    #    )
    remind_on_date = forms.DateField(help_text="For All Dates: use 'YYYY-MM-DD' Format")

    class Meta:
        model = reminder
        fields = ('owner', 'email', 'car', 'msg', 'remind_on_date')

    def __init__(self, user, *args, **kwargs):
        super(reminderForm, self).__init__(*args, **kwargs)
        self.fields['car'].queryset = car.objects.filter(owner=user.get_username())
