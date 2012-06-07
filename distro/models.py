# -*- coding: utf-8 -*-
from django.db import models
'''
modelos das tabelas da aplicação
'''

class TipoContrato(models.Model):
    '''
    TipoContrato - tipo de contrato do docente
    '''
    nome = models.CharField(max_length=80)
    pass


class Categoria(models.Model):
    '''
    Categoria - representação da categoria profissional do 
    docente
    '''
    nome = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nome
    pass
    

class UnidadeOrganica(models.Model):
    '''
    UnidadeOrganica - unidades organicas do IPBeja
    '''
    nome = models.CharField(max_length=80)
    abreviatura = models.CharField(max_length=4)
    def __unicode__(self):
        return self.abreviatura + '- ' + self.nome
    pass

class Departamento(models.Model):
    '''
    Departamento - departamentos do IPBeja
    '''
    nome = models.CharField(max_length=80)
    abreviatura = models.CharField(max_length=4)
    sede = models.ForeignKey('UnidadeOrganica')

    def __unicode__(self):
        return self.abreviatura + '- ' + self.nome
    pass
    
class TipoCurso(models.Model):
    '''
    TipoCurso - tipo de curso do IPBeja
    '''
    nome = models.CharField(max_length=40)
    abreviatura = models.CharField(max_length=4)
    
    def __unicode__(self):
        return self.abreviatura + '- ' + self.nome
    pass

class Curso(models.Model):
    '''
    Curso - curso em funcionamento no IPBeja
    '''
    nome = models.CharField(max_length=40)
    abreviatura = models.CharField(max_length=4)
    tipo_curso = models.ForeignKey('TipoCurso')

    def __unicode__(self):
        return unicode(self.abreviatura) + '- ' + unicode(self.nome)
    pass
    
