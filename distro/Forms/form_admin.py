# -*- coding: utf-8 -*-
'''
Created on 26/02/2014

@author: admin1
'''
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _


class AddUserForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': _(u"O nome de utilizador inserido já existe."),
        'password_mismatch': _(u"Os dois campos da palavra-chave são diferentes."),
    }
    
    first_name  = forms.CharField(required = False, max_length=150, label=u'Primeiro Nome', \
                                        widget=forms.TextInput(attrs={'class':'form-control colorInput tamanhoInput'}))
    
    last_name  = forms.CharField(required = False, max_length=150, label=u'Último Nome', \
                                        widget=forms.TextInput(attrs={'class':'form-control colorInput tamanhoInput'}))
    email = forms.EmailField(max_length=300, label=_(u'E-mail'), widget=forms.TextInput(attrs={'class':'form-control tamanhoInput'}))
    
    username = forms.RegexField(label=_("Nome Utilizador"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages = {
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")}, widget=forms.TextInput(attrs={'class':'form-control colorInput tamanhoInput'}))
    
    
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs={'class':'form-control colorInput tamanhoInput'}))
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class':'form-control colorInput tamanhoInput'}),
        help_text = _("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    #===========================================================================
    # def save(self, commit=True):
    #     user = super(AddUserForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     if commit:
    #         user.save()
    #     return user
    #===========================================================================


class UserChangeForm(forms.ModelForm):
    username = forms.RegexField(
        label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
        help_text = _("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages = {
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    def clean_password(self):
        return self.initial["password"]

    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')