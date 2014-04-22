# -*- coding: utf-8 -*-
'''
Created on 26/02/2014

@author: admin1
'''
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User, Permission, Group
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext, ugettext_lazy as _


# Cria o form de criação de grupos
class AddGroupForm(forms.Form):
        
    name = forms.CharField(max_length = 300, label = _(u'Nome do grupo'), widget = forms.TextInput(attrs = {'class':'form-control colorInput tamanhoInput'}))
    
    perm = forms.ModelMultipleChoiceField(queryset = Permission.objects.all(), label = _(u'Permissões'), widget = forms.SelectMultiple(attrs = {'multiple class':'form-control colorInput tamanhoInputMultipleSelect'}))
    
    class Meta:
        model = Group
        pass


# Formulario para adicionar utilizador
class AddUserForm(forms.Form):
    error_messages = {
        'duplicate_username': _(u"O nome de utilizador inserido já existe."),
        'password_mismatch': _(u"Os dois campos da palavra-chave são diferentes."),
    }
    
    first_name = forms.CharField(required = False, max_length = 150, label = u'Primeiro Nome', \
                                        widget = forms.TextInput(attrs = {'class':'form-control colorInput tamanhoInput'}))
    
    last_name = forms.CharField(required = False, max_length = 150, label = u'Último Nome', \
                                        widget = forms.TextInput(attrs = {'class':'form-control colorInput tamanhoInput'}))
    email = forms.EmailField(max_length = 300, \
                             label = _(u'E-mail'),
                             widget = forms.TextInput(attrs = {'class':'form-control colorInput tamanhoInput', \
                                                               "autocomplete": "off"}))
    
    username = forms.RegexField(label = _("Nome Utilizador"), max_length = 30,
        regex = r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages = {
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")}, widget = forms.TextInput(attrs = {'class':'form-control colorInput tamanhoInput', "autocomplete": "off"}))
    
    is_active = forms.BooleanField(label = _("Activo"), required = False, initial = True, \
                    widget = forms.CheckboxInput(attrs = {'class':'form-control tamanhoInput colorInput'}))
    
    password1 = forms.CharField(label = _("Password"),
        widget = forms.PasswordInput(attrs = {'class':'form-control colorInput tamanhoInput', "autocomplete": "off"}))
    password2 = forms.CharField(label = _("Password confirmation"),
        widget = forms.PasswordInput(attrs = {'class':'form-control colorInput tamanhoInput'}),
        help_text = _("Enter the same password as above, for verification."))
    
    group = forms.ModelChoiceField(required = False, \
                   queryset = Group.objects.all(), \
                   label = _(u'Grupos'), \
                   widget = forms.Select(
                               attrs = {'class':'form-control colorInput tamanhoInput'}))

    # class Meta:
    #    model = User
    #    fields = ("first_name", "last_name", "email", "username", "is_active")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username = username)
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
    


class EditUserForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': _(u"O nome de utilizador inserido já existe."),
        'password_mismatch': _(u"Os dois campos da palavra-chave são diferentes."),
    }
    
    first_name = forms.CharField(required = False, max_length = 150, label = u'Primeiro Nome', \
                                        widget = forms.TextInput(attrs = {'class':'form-control colorInput tamanhoInput'}))
    
    last_name = forms.CharField(required = False, max_length = 150, label = u'Último Nome', \
                                        widget = forms.TextInput(attrs = {'class':'form-control colorInput tamanhoInput'}))
    email = forms.EmailField(max_length = 300, label = _(u'E-mail'), widget = forms.TextInput(attrs = {'class':'form-control tamanhoInput'}))
    
    username = forms.RegexField(label = _("Nome Utilizador"), max_length = 30,
        regex = r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages = {
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")}, widget = forms.TextInput(attrs = {'class':'form-control colorInput tamanhoInput'}))
    is_active = forms.BooleanField(label = _("Activo"), required = False, initial = True, \
                    widget = forms.CheckboxInput(attrs = {'class':'form-control tamanhoInput colorInput'}))
    
    group = forms.ModelChoiceField(required = False, \
                   queryset = Group.objects.all(), \
                   label = _(u'Grupos'), \
                   widget = forms.Select(
                               attrs = {'class':'form-control colorInput tamanhoInput'}))
    
    def __init__(self, username, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.username = username
    
    
    # class Meta:
        # model = User
        # fields = ("first_name", "last_name", "email", "username")

    def clean_username(self):
        username = self.cleaned_data["username"]
        print "username", username, type(username) 
        print "self.username", self.username, type(username)
        if self.username != username:
            print "IF"
            try:
                User.objects.get(username = username)
            except User.DoesNotExist:
                return username
            raise forms.ValidationError(self.error_messages['duplicate_username'])
        else:
            print "else"
            return username
 

# Actualizar Password.
class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without entering the
    old password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label = _("New password"),
                                    widget = forms.PasswordInput(attrs = {'class':'form-control colorInput tamanhoInput'}))
    new_password2 = forms.CharField(label = _("New password confirmation"),
                                    widget = forms.PasswordInput(attrs = {'class':'form-control colorInput tamanhoInput'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return password2

    def save(self, commit = True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

# FORM para os utilizadores poderem alterar a sua passord
class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change his/her password by entering
    their old password.
    """
    error_messages = {
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
    }
    old_password = forms.CharField(label = _("Old password"),
                                   widget = forms.PasswordInput(attrs = {'class':'form-control colorInput tamanhoInput'}))

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'])
        return old_password

PasswordChangeForm.base_fields = SortedDict([
    (k, PasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
])


# Reset a password por parte do administrador.
class PasswordChangeFormReset(forms.Form):
    """
    A form used to change the password of a user in the admin interface.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label = _("Password"),
                                widget = forms.PasswordInput(attrs = {'class':'form-control colorInput tamanhoInput'}))
    password2 = forms.CharField(label = _("Password (again)"),
                                widget = forms.PasswordInput(attrs = {'class':'form-control colorInput tamanhoInput'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordChangeFormReset, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return password2

    def save(self, commit = True):
        """
        Saves the new password.
        """
        self.user.set_password(self.cleaned_data["password1"])
        if commit:
            self.user.save()
        return self.user




#===============================================================================
# class UserChangeForm(forms.ModelForm):
#     username = forms.RegexField(
#         label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
#         help_text = _("Required. 30 characters or fewer. Letters, digits and "
#                       "@/./+/-/_ only."),
#         error_messages = {
#             'invalid': _("This value may contain only letters, numbers and "
#                          "@/./+/-/_ characters.")})
#     password = ReadOnlyPasswordHashField(label=_("Password"),
#         help_text=_("Raw passwords are not stored, so there is no way to see "
#                     "this user's password, but you can change the password "
#                     "using <a href=\"password/\">this form</a>."))
# 
#     def clean_password(self):
#         return self.initial["password"]
# 
#     class Meta:
#         model = User
# 
#     def __init__(self, *args, **kwargs):
#         super(UserChangeForm, self).__init__(*args, **kwargs)
#         f = self.fields.get('user_permissions', None)
#         if f is not None:
#             f.queryset = f.queryset.select_related('content_type')
#===============================================================================
