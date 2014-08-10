# -*- coding: utf-8 -*-
'''
Created on 26/07/2014

@author: Carlos Rijo Palma
@email: carlosrijopalma@hotmail.com
@author: António Urbano Baião
@email: baiao@sapo.pt
'''

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from distro.models import Ano, TipoCurso, Curso


class Combobox_geral_Statistics(forms.Form):
    MY_CHOICES = (('', '-----'),
                  ('1', 'Curso'),
                  ('2', 'Turma'),
                  ('3', 'Disciplina'),
                  ('4', 'Docente'),
                  )
                
    combobox_Geral_option = forms.ChoiceField(choices = MY_CHOICES, \
                                              label = _(u'Tipo Estatística'), \
                                              widget=forms.Select(attrs={'class':'form-control colorInput size_30_percent'}))

class Estatistica_docente(forms.Form):
    MY_CHOICES = (('', '-----'),
                  ('1', 'Por Hora'),
                  ('2', 'Por Curso'),
                  ('3', 'Por Turma'),
                  ('4', 'Por Disciplina'),
                  )
                
    tipo_docente = forms.ChoiceField(choices = MY_CHOICES, \
                                              label = _(u'Docente'), \
                                              widget=forms.Select(attrs={'class':'form-control colorInput size_30_percent'}))
    
    

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
    def __init__(self, value, *args, **kwargs):
        super(Combobox_hora, self).__init__(*args, **kwargs)
        if value:
            self.fields['horas_maximo'] = forms.IntegerField(required = False)
            self.fields['horas_maximo'].widget = forms.TextInput(attrs={'class': 'colorInput size_medio'})
        else:
            self.fields['horas'] = forms.IntegerField(required = False)
            self.fields['horas'].widget = forms.TextInput(attrs={'class': 'colorInput size_medio'})
    


class Tipo_Curso_Form(forms.Form):
    tipo_curso = forms.ModelChoiceField(TipoCurso.objects.all(), \
                                        label = _(u"Tipo Curso"), \
                                        widget = forms.Select(attrs = {'class':'form-control colorInput size_50_percent'}))


class Cursos_Forn(forms.Form):
    cursoList = forms.ModelChoiceField(Curso.objects.all(), \
                                       widget = forms.Select(attrs={'class': 'form-control colorInput size_50_percent'}))
    
    def __init__(self, query, *args, **kwargs):
        super(Cursos_Forn, self).__init__(*args, **kwargs)
        self.fields['cursoList'].queryset = query
        #self.fields['cursoList'].widget = forms.Select(attrs={'class': 'form-control colorInput size_50_percent'})
        self.fields['cursoList'].label = _(u"Curso")
    
    
    
    
    
    
