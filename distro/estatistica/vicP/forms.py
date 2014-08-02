# -*- coding: utf-8 -*-
'''
Created on 26/07/2014

@author: Carlos Rijo Palma
@email: carlosrijopalma@hotmail.com
@author: António Urbano Baião
@email: baiao@sapo.pt
'''

from distro.models import Ano
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _




class Combobox_geral_Statistics(forms.Form):
    MY_CHOICES = (('', '-----'),
                  ('1', 'Curso'),
                  ('2', 'Turma'),
                  ('3', 'Disciplina'),
                  ('4', 'Docente'),
                  )
                
    combobox_Geral_option = forms.ChoiceField(choices = MY_CHOICES, \
                                              label = _(u'Tipo Estatística'), \
                                              widget=forms.Select(attrs={'class':'form-control colorInput'}))


class Estatistica_docente(forms.Form):
    MY_CHOICES = (('', '-----'),
                  ('1', 'Por Hora'),
                  ('2', 'Por Curso'),
                  ('3', 'Por Turma'),
                  ('4', 'Por Disciplina'),
                  )
                
    tipo_docente = forms.ChoiceField(choices = MY_CHOICES, \
                                              label = _(u'Docente'), \
                                              widget=forms.Select(attrs={'class':'form-control colorInput'}))
    
    

# Combox para a estatistica de Docente por hora
class Docente_hora(forms.Form):
    
    
    CHOICES=[('0','Mais de'),
             ('1','Menos de'),
             ('2','Entre as')
             ]

    valor = forms.ChoiceField(choices=CHOICES, \
                              label = _(u"Com"), \
                              widget=forms.RadioSelect())
    #===========================================================================
    #     
    # maior = forms.BooleanField(label = _(u'Mais'), \
    #                 widget=forms.CheckboxInput(attrs={'class':'form-control colorInput'}))
    # menor = forms.BooleanField(label = _(u'Menos'), \
    #                 widget=forms.CheckboxInput(attrs={'class':'form-control colorInput'}))
    # 
    # entreHoras = forms.BooleanField(label = _(u'Entre Horas'), \
    #                 widget=forms.CheckboxInput(attrs={'class':'form-control colorInput'}))
    #===========================================================================
    

class Combobox_hora(forms.Form):
    horas = forms.IntegerField(required=False, \
                               widget=forms.TextInput(attrs={'class':'colorInput size_medio', \
                                                             'autofocus':"autofocus"}) )
    
    
    def __init__(self, label, *args, **kwargs):
        super(Combobox_hora, self).__init__(*args, **kwargs)
        self.fields['horas'].label = label
    
