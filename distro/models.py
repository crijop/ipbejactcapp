# -*- coding: utf-8 -*-
from django.db import models
'''
modelos das tabelas da aplicação
'''

import datetime

class TipoContrato(models.Model):
    '''
    TipoContrato - tipo de contrato do docente
    '''
    TIPO_CONTRATO_CHOICES = (
        ('RQ', u'Requisição'),
        ('ST', u'Sem termo'),
        ('TC', u'Termo Certo'),
        ('NM', u'Nomeação'),
        ('PL', u'Preleção'),
    )
    nome = models.CharField(max_length=80, 
                            choices=TIPO_CONTRATO_CHOICES)

    def __unicode__(self):
        return self.nome

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
        # return self.abreviatura + '- ' + self.nome
        return self.nome
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
        # return unicode(self.abreviatura) + '- ' + unicode(self.nome)
        return unicode(self.nome)
    pass
    
class Cnaef(models.Model):
    '''
    códigos cnaef
    '''
    nome = models.CharField(max_length=120, 
                            blank=True, 
                            null=True,
                            default=" ")
    codigo = models.CharField(max_length=20,
                              unique=True)
    def __unicode__(self):
        return unicode(self.codigo) + '- ' + unicode(self.nome)
    pass
    
class GrauAcademico(models.Model):
    '''
    graus académicos em geral
    '''
    titulo = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.codigo) # + '- ' + unicode(self.nome)
    pass
    

class Epoca(models.Model):
    '''
    '''
    EPOCA_CHOICES = (
        ('O', u'Outono'),
        ('P', u'Primavera'),
    )
    nome = models.CharField(max_length=20, choices=EPOCA_CHOICES)
    abreviatura = models.CharField(max_length=1)

    def __unicode__(self):
        return unicode(self.abreviatura) + '- ' + unicode(self.nome)
    pass
    
    
class UnidadeCurricular(models.Model):
    '''
    unidades curriculares
    '''
    # caracterização da unidade curricular
    nome         = models.CharField(max_length=120)
    curso        = models.ForeignKey('Curso')
    departamento = models.ForeignKey('Departamento')
    cnaef        = models.ForeignKey('Cnaef', null=True)
    ects         = models.FloatField(default=0, null=True)
    ano          = models.IntegerField(default=0, null=True)
    semestre     = models.IntegerField(default=0, null=True)
    epoca        = models.ForeignKey('Epoca')

    # horas de uma unidade curricular
    horas_lei_t  = models.FloatField(default=0, null=True)
    horas_lei_tp = models.FloatField(default=0, null=True)
    horas_lei_pl = models.FloatField(default=0, null=True)
    horas_lei_tc = models.FloatField(default=0, null=True)
    horas_lei_s  = models.FloatField(default=0, null=True)
    horas_lei_e  = models.FloatField(default=0, null=True)
    horas_lei_ot = models.FloatField(default=0, null=True)
    horas_lei_o  = models.FloatField(default=0, null=True)

    data_modificacao = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.curso) + '- ' + unicode(self.nome)
    pass


class Reducao(models.Model):
    '''
    cargos e outros tipos de redução
    '''
    nome        = models.CharField(max_length=120, unique=True)
    horas       = models.IntegerField(default=0, null=True)

    data_modificacao = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.nome)
    pass

class Docente(models.Model):
    '''
    caraterização de docente
    '''
    nome_completo     = models.CharField(max_length=300)
    departamento      = models.ForeignKey('Departamento')
    categoria         = models.ForeignKey('Categoria')
    percentagem       = models.IntegerField(default=100, 
                                            blank=True,
                                            null=True)
    tipo_contrato     = models.ForeignKey('TipoContrato')

    data_inicio = models.DateField(null=True,
                                   default=datetime.\
                                       date(year=1980,
                                            month=1,
                                            day=1))
    data_fim = models.DateField(null=True,
                                default=datetime.\
                                    date(year=2050,
                                         month=1,
                                         day=1))

    data_modificacao = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.nome_completo)
    pass

class Titulo(models.Model):
    '''
    titulo académico
    '''
    TITULO_CHOICES = (
        ('AG', u'Agregado'),
        ('DT', u'Doutor'),
        ('MS', u'Mestre'),
        ('LI', u'Licenciado'),
        ('BA', u'Bacharel'),
        ('DU', u'Docteur'),
        ('PH', u'PhD'),
        ('D1', u'Doctor'),
        ('D1', u'Especialista'),
        ('M1', u'MSc'),
        )

    nome = models.CharField(max_length=100,
                            unique=True,
                            choices=TITULO_CHOICES)
    def __unicode__(self):
        return unicode(self.nome) 

    pass


class CursoDocente(models.Model):
    '''
    curso do docente
    junção de cursos de docentes
    '''
    docente = models.ForeignKey('Docente')
    titulo  = models.ForeignKey('Titulo')
    curso   = models.CharField(max_length=200)
    instituicao = models.CharField(max_length=200)
    cnaef = models.ForeignKey('Cnaef')

    def __unicode__(self):
        return unicode(self.docente) + '- ' + \
            unicode(self.titulo) + ' ' + \
            unicode(self.curso)
    pass


#class Turma(models.Model):
    
# class Distribuicao(models.Model):
#     '''
#     representacao de uma distribuicao de serviço
#     docente
#     '''
#     docente = models.ForeignKey('Docente')

