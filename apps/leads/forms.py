from .models import LEADS
from django import forms
from django.forms import ModelForm

from ..users.models import MyUser
from .models import LEADS
from django.db.models import Q

import re


class CreateForm(ModelForm):
    description = forms.CharField(

        label='Description',

        widget=forms.Textarea()
    )
    website=forms.URLField()
    x=0;

    # def save(self,*args,**kwargs):
    #     if not self.instance.pk:
    #         super(CreateForm, self).save(*args, **kwargs)
    #



    def clean_company_name(self):
        data = self.cleaned_data.get('company_name')
        data = data.strip().title()
        if re.match(r'^[A-Za-z-&_]+$', data):
            return data
        else:
            raise forms.ValidationError("Only alphabets are allowed")

    def clean_contact_person(self):
        data = self.cleaned_data.get('contact_person')
        if re.match('^[a-zA-Z]*$', data):
            return data
        else:
            raise forms.ValidationError("Only alphabets are allowed")

    def clean_source(self):
        data = self.cleaned_data.get('source')
        if re.match('^[a-zA-Z-&_:,]*$', data):
            return data
        else:
            raise forms.ValidationError("Input is not allowed \n Input can be alphabets and special character like:&,-,_:,comma ")

    def clean_source_type(self):
        data = self.cleaned_data.get('source_type')
        if re.match('^[a-zA-Z-&_:,]*$', data):
            return data
        else:
            raise forms.ValidationError(
                "Input is not allowed \n Input can be alphabets and special character like:&,-,_:,comma ")

    def clean_description(self):
        data = self.cleaned_data.get('description')
        if re.match('^[a-zA-Z-&_:,]*$', data):
            return data
        else:
            raise forms.ValidationError(
                "Input is not allowed \n Input can be alphabets and special character like:&,-,_:,comma ")


    def clean_email(self):
        data = self.cleaned_data.get('email')

        # user_id = self.initial.get("logged_user")

        if self.instance.pk is not None:
            LEADS.objects.get(email=data)
            raise forms.ValidationError("Email already exists")
        else:
            return data









    def clean_contact_number(self):
        data = self.cleaned_data.get('contact_number')
        if data == None:
            pass
        else:
            data = str(data)
            print(data)
            if re.search('[+-]', data):
                raise forms.ValidationError("'+', '-' are not allowed")
            elif len(data) == 10:
                return data
            else:
                raise forms.ValidationError("Please enter a 10 digit number")

    class Meta:
        model = LEADS
        fields = ('contact_number','company_name','description','website','contact_person','source','source_type','email','assigned_boolean')

class UpdateForm(ModelForm):
    description = forms.CharField(

        label='Description',

        widget=forms.Textarea()
    )
    website=forms.URLField()
    x=0;

    # def save(self,*args,**kwargs):
    #     if not self.instance.pk:
    #         super(CreateForm, self).save(*args, **kwargs)
    #



    def clean_company_name(self):
        data = self.cleaned_data.get('company_name')
        data = data.strip().title()
        if re.match(r'^[A-Za-z-&_]+$', data):
            return data
        else:
            raise forms.ValidationError("Only alphabets are allowed")

    def clean_contact_person(self):
        data = self.cleaned_data.get('contact_person')
        if re.match('^[a-zA-Z]*$', data):
            return data
        else:
            raise forms.ValidationError("Only alphabets are allowed")

    def clean_source(self):
        data = self.cleaned_data.get('source')
        if re.match('^[a-zA-Z-&_:,]*$', data):
            return data
        else:
            raise forms.ValidationError("Input is not allowed \n Input can be alphabets and special character like:&,-,_:,comma ")

    def clean_source_type(self):
        data = self.cleaned_data.get('source_type')
        if re.match('^[a-zA-Z-&_:,]*$', data):
            return data
        else:
            raise forms.ValidationError(
                "Input is not allowed \n Input can be alphabets and special character like:&,-,_:,comma ")

    def clean_description(self):
        data = self.cleaned_data.get('description')
        if re.match('^[a-zA-Z-&_:,]*$', data):
            return data
        else:
            raise forms.ValidationError(
                "Input is not allowed \n Input can be alphabets and special character like:&,-,_:,comma ")


    def clean_email(self):
        data = self.cleaned_data.get('email')
        return data

        # user_id = self.initial.get("logged_user")











    def clean_contact_number(self):
        data = self.cleaned_data.get('contact_number')
        if data == None:
            pass
        else:
            data = str(data)
            print(data)
            if re.search('[+-]', data):
                raise forms.ValidationError("'+', '-' are not allowed")
            elif len(data) == 10:
                return data
            else:
                raise forms.ValidationError("Please enter a 10 digit number")

    class Meta:
        model = LEADS
        fields = ('contact_number','company_name','description','website','contact_person','source','source_type','email','assigned_boolean')


class DetailForm(forms.Form):
    assign = forms.ModelChoiceField(

        queryset=MyUser.objects.filter(department='Marketing'),
        empty_label="selected employee"

    )

    class Meta:
        model=LEADS
        fields='__all__'






