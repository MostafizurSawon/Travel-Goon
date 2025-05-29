from django import forms
from .models import TravelAgencyCV, Language, PassportInfo
from django_select2.forms import Select2TagWidget

class TravelAgencyCVForm(forms.ModelForm):
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        required=False,
        label='Languages',
        widget=Select2TagWidget(attrs={'class': 'form-control', 'style': 'width:100%;'})
    )

    class Meta:
        model = TravelAgencyCV
        exclude = ['user']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name_bn': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),  # Add bio here
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'blood_group_other': forms.TextInput(attrs={'class': 'form-control'}),
            'language_other': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'current_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_permanent_same_as_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fathers_name': forms.TextInput(attrs={'class': 'form-control'}),
            'fathers_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'fathers_nid': forms.TextInput(attrs={'class': 'form-control'}),
            'mothers_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mothers_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'mothers_nid': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'married': forms.Select(attrs={'class': 'form-select'}),
            'last_education': forms.Select(attrs={'class': 'form-select'}),
            'last_education_other': forms.TextInput(attrs={'class': 'form-control'}),
            'last_education_result': forms.TextInput(attrs={'class': 'form-control'}),
            'last_education_passing_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_job_status': forms.Select(attrs={'class': 'form-select'}),
            'current_job_status_other': forms.TextInput(attrs={'class': 'form-control'}),
            'current_job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class PassportInfoForm(forms.ModelForm):
    class Meta:
        model = PassportInfo
        fields = [
            'passport_number', 'full_name', 'date_of_birth', 'place_of_birth', 
            'nationality', 'gender', 'father_name', 'mother_name', 
            'spouse_name', 'issue_date', 'expiry_date', 'place_of_issue', 
            'passport_photo', 'signature'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }
