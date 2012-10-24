# -*- coding: utf-8 -*-
'''
Created on 15 de Out de 2012

@author: admin1
'''
from distro.models import Turma, ServicoDocente, Docente, UnidadeCurricular
from django import forms
from django.core.context_processors import request
from django.forms.models import ModelForm



class AdicionarServicoDocenteForm(ModelForm):
    '''
    def __init__(self, *args, **kwargs):
        id_D = kwargs.pop('id_Departamento')
        ano = kwargs.pop('ano')
        super(AdicionarServicoDocenteForm, self).__init__(*args, **kwargs)
    '''    
        
        #self.fields['turma'] = forms.ModelChoiceField(
        #                Turma.objects.filter(unidade_curricular__departamento_id__exact = id_Departamento).filter(ano = ano)
        #                )
        
        #=======================================================================
        # self.fields['docente'] = forms.ModelChoiceField(Docente.objects.filter(departamento_id__exact = id_D),
        #                                  widget = forms.Select(attrs = {'onchange':'testeSearch();'}))
        # self.fields['horas'] = forms.CharField(widget=forms.TextInput(attrs={ 'readonly': 'readonly' }))
        #=======================================================================
        
    def is_valid(self, listaModulos, listaDocentes):
        """
        Returns True if the form has no errors. Otherwise, False. If errors are
        being ignored, returns False.
        """
        if listaDocentes != None:
            
            sizeModulos = len(listaModulos)
            cont = 0
            for docente in listaDocentes:
                if docente != "":
                    cont +=1
                    pass
                pass
            
            if sizeModulos == cont:
                return True
            else:
                return False
            pass
        else:
            return False

    class Meta:
        model = ServicoDocente
        exclude = ('turma', 'horas')
        
     
    pass