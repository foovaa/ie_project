from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Employees
from django.contrib.auth.models import User

class EmployeeCreateForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('female', 'Female'),
        ('male', 'Male'),
        ('none', 'None'),
    )

    name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    age =forms.IntegerField(required=True, min_value=18, max_value=70)
    national_id = forms.CharField(max_length=10, required=True)
    personal_id = forms.CharField(max_length=10, required=True)
    tele = PhoneNumberField(required=True)
    address = forms.CharField(max_length=200, required=True, widget=forms.Textarea(attrs={'rows': 2, 'cols': 20}))
    salary = forms.IntegerField(max_value=1000000000, min_value=1000, required=True)
    is_married = forms.BooleanField(required=False)
    gender = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.RadioSelect)


    class Meta:
        model = Employees
        fields = "__all__"
        # fields = ('name',
        #           'last_name',
        #           'national_id',
        #           'personal_id',
        #           'tele',
        #           'address',
        #           'is_married',
        #           'salary', )

    def clean_national_id(self):
        n_id = self.cleaned_data['national_id']
        if not n_id.isdigit():
            raise forms.ValidationError('the personal id is number field!')
        if len(n_id) != 10:
            raise forms.ValidationError('please inter 10 digits...')
        return n_id


    def clean_personal_id(self):
        p_id = self.cleaned_data['personal_id']
        if not p_id.isdigit():
            raise forms.ValidationError('the personal id is number field!')
        if len(p_id) != 10:
            raise forms.ValidationError('please inter 10 digits...')
        return p_id


class UpdateEmployee(EmployeeCreateForm):
    # personal_id = forms.CharField(Field.disabled=True
    def __init__(self, *args, **kwargs):
        super(UpdateEmployee, self).__init__(*args, **kwargs)
        self.fields['personal_id'].disabled = True


# class LoginForm(forms.ModelForm):
#     username = forms.CharField()
#     password = forms.CharField()

#     class Meta:
#         model = User
#         fields = ('username', 'password')


class FilterForm(forms.Form):
    name = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'style': 'margin-right: 30px;'}))
    age = forms.IntegerField(min_value=18, max_value=70, required=False)
    is_married = forms.BooleanField(required=False)

class FindForm(forms.Form):
    personal_id = forms.CharField(max_length=10, required=False)

    def clean_personal_id(self):
        p_id = self.cleaned_data['personal_id']
        if not p_id.isdigit():
            raise forms.ValidationError('the personal id is number field!')
        if len(p_id) != 10:
            raise forms.ValidationError('please inter 10 digits...')
        return p_id















