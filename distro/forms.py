# -*- coding: utf-8 -*-
'''
Created on 20 de Set de 2012

@author: admin1
'''


from django import forms
from distro.models import Departamento

class AddDocenteForm(forms.Form):
    nome_completo     = forms.CharField(max_length=300)
                                         
    
    departamento      = forms.ModelChoiceField(queryset=Departamento.objects.all())

    # escalao de vencimento do docente
    escalao           = forms.IntegerField()

    regime_exclusividade = forms.BooleanField(required=False)

    email = forms.EmailField()
    
    abreviatura       = forms.CharField()

    # foto = forms.ImageField()