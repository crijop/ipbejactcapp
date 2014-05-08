# -*- coding: utf-8 -*-
'''
Created on 08/05/2014

@author: Carlos Rijo Palma
@author: António Urbano Baião
'''
from distro.models import Ano
from django import forms


# Combox para 
class ComboxAno(forms.Form):
    ano = forms.ModelChoiceField(queryset = Ano.objects.all(), required = True, \
                              label = 'Ano', widget = forms.Select(
                              attrs = {'class':'form-control colorInput', "onchange" : "$('#filter_ano_form').submit()", "name":"ano"}))
    
    def __init__(self, listaAnos, *args, **kwargs):
        super(ComboxAno, self).__init__(*args, **kwargs)
        self.fields['ano'].queryset = listaAnos
