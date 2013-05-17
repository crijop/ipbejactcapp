# -*- coding: utf-8 -*-
'''
Created on 15 de Mai de 2013

@author: admin1
'''
from distro.models import Curso, TipoCurso
from django import forms
from django.forms.models import ModelForm


class AdicionarCursoForm(ModelForm):
    nome = forms.CharField(max_length=100, label=u'Nome do Curso')
    abreviatura = forms.CharField(max_length=4)
    
    tipo_curso = forms.ModelChoiceField(label="Tipo de Curso", queryset=TipoCurso.objects.all(), empty_label=" ")#,
    #widget = forms.Select(attrs = {'onchange':'testeSearch();'}))
    semestre_letivos = forms.IntegerField(label="Semestres Letivos", initial=2)
    
    class Meta:
        model = Curso
        pass
    pass
