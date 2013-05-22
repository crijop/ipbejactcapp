# -*- coding: utf-8 -*-
'''
Created on 15 de Mai de 2013

@author: admin1
'''
from distro.models import Curso, TipoCurso
from django import forms
from django.forms.models import ModelForm

class AdicionarCursoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        
        tipoCurso = kwargs.pop('tipoCurso')
        super(AdicionarCursoForm, self).__init__(*args, **kwargs)
    
        self.fields['nome'] = forms.CharField(max_length=100, label=u'Nome do Curso')
        self.fields['abreviatura'] = forms.CharField(max_length=4)
        self.fields['tipo_curso'] = forms.ModelChoiceField(widget=forms.Select(attrs={'class':"selectTipoCurso", 'onchange':'this.form.action=this.form.submit()'}), label="Tipo de Curso", queryset=TipoCurso.objects.filter(id=tipoCurso), empty_label=None)
        self.fields['semestre_letivos'] = forms.IntegerField(label="Semestres Letivos", initial=2)
        
    class Meta:
        model = Curso
        fields = ('nome', 'abreviatura', 'tipo_curso', 'semestre_letivos')
        pass
    pass
