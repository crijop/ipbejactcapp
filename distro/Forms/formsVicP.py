# -*- coding: utf-8 -*-
'''
Created on 15 de Mai de 2013

@author: admin1
'''
from distro.models import Curso
from django import forms
from django.forms.models import ModelForm


class AdicionarCursoForm(ModelForm):
    nome = forms.CharField(max_length=100, label=u'Nome do Curso')
    abreviatura = forms.CharField(max_length=4)
    #tipo_curso = forms.ForeignKey('TipoCurso')

    # número de semestres letivos de um curso
    #semestre_letivos = forms.IntegerField(default=2)
    
    class Meta:
        model = Curso
        pass
    pass
