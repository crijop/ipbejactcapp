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
    nome = models.CharField(max_length = 80,
                            choices = TIPO_CONTRATO_CHOICES,
                            help_text = "contratação ao abrigo da lei")

    def __unicode__(self):
        return self.nome

    pass

class Categoria(models.Model):
    '''
    Categoria - representação da categoria profissional do 
    docente
    '''
    nome = models.CharField(max_length = 100,
                            unique = True,
                            help_text = "categorias do ensino superior")

    def __unicode__(self):
        return unicode(self.nome)
    pass
    

class UnidadeOrganica(models.Model):
    '''
    UnidadeOrganica - unidades organicas do IPBeja
    '''
    nome = models.CharField(max_length = 80,
                            unique = True)
    abreviatura = models.CharField(max_length = 4,
                                   unique = True)

    def __unicode__(self):
        return unicode(self.nome)

    class Meta:
        verbose_name_plural = "unidades orgânicas"
        pass

    pass

class Departamento(models.Model):
    '''
    Departamento - departamentos do IPBeja
    '''
    nome = models.CharField(max_length = 80, unique = True)
    abreviatura = models.CharField(max_length = 4, unique = True)
    sede = models.ForeignKey('UnidadeOrganica',
                             help_text = "os departamentos encontram-se sedeados em unidades orgânicas")

    def __unicode__(self):
        # return self.abreviatura + '- ' + self.nome
        return self.nome
    pass
    
class TipoCurso(models.Model):
    '''
    TipoCurso - tipo de curso do IPBeja
    '''
    nome = models.CharField(max_length = 40, unique = True)
    abreviatura = models.CharField(max_length = 4, unique = True)
    
    def __unicode__(self):
        return self.abreviatura + ' - ' + self.nome
    pass

class Curso(models.Model):
    '''
    Curso - curso em funcionamento no IPBeja
    '''
    nome = models.CharField(max_length = 40)
    abreviatura = models.CharField(max_length = 4)
    tipo_curso = models.ForeignKey('TipoCurso')

    # número de semestres letivos de um curso
    semestre_letivos = models.IntegerField(default = 2)

    def __unicode__(self):
        # return unicode(self.abreviatura) + '- ' + unicode(self.nome)
        return unicode(self.nome)
    pass
    
class Cnaef(models.Model):
    '''
    códigos cnaef
    '''
    nome = models.CharField(max_length = 120,
                            blank = True,
                            null = True,
                            default = " ")
    codigo = models.CharField(max_length = 20,
                              unique = True)
    def __unicode__(self):
        return unicode(self.codigo) + '- ' + unicode(self.nome)
    class Meta:
        verbose_name_plural = "CNAEF"
    pass
    
class GrauAcademico(models.Model):
    '''
    graus académicos em geral
    '''
    titulo = models.CharField(max_length = 20)

    def __unicode__(self):
        return unicode(self.titulo)  # + '- ' + unicode(self.nome)
    pass
    

class Epoca(models.Model):
    '''
    '''
    EPOCA_CHOICES = (
        ('O', u'Outono'),
        ('P', u'Primavera'),
    )
    nome = models.CharField(max_length = 20, choices = EPOCA_CHOICES)
    abreviatura = models.CharField(max_length = 1)

    def __unicode__(self):
        return unicode(self.abreviatura) + '- ' + unicode(self.nome)

    class Meta:
        verbose_name_plural = "épocas"

    pass
    
    
class UnidadeCurricular(models.Model):
    '''
    unidades curriculares
    '''
    # caracterização da unidade curricular
    nome = models.CharField(max_length = 120)
    curso = models.ForeignKey('Curso')
    departamento = models.ForeignKey('Departamento')
    cnaef = models.ForeignKey('Cnaef', null = True)
    ects = models.FloatField(default = 0, null = True)
    ano = models.IntegerField(default = 1, null = True)
    semestre = models.IntegerField(default = 1, null = True)
    epoca = models.ForeignKey('Epoca',
                                     default = 1,
                                     null = True)

    # horas de uma unidade curricular
    horas_lei_t = models.IntegerField(default = 0, null = True, blank = True)
    horas_lei_tp = models.IntegerField(default = 0, null = True, blank = True)
    horas_lei_pl = models.IntegerField(default = 0, null = True, blank = True)
    horas_lei_tc = models.IntegerField(default = 0, null = True, blank = True)
    horas_lei_s = models.IntegerField(default = 0, null = True, blank = True)
    horas_lei_e = models.IntegerField(default = 0, null = True, blank = True)
    horas_lei_ot = models.IntegerField(default = 0, null = True, blank = True)
    horas_lei_o = models.IntegerField(default = 0, null = True, blank = True)

    data_modificacao = models.DateTimeField(auto_now = True)

    # regente da unidade curricular
    regente = models.ForeignKey('Docente',
                                null = True,
                                blank = True)

    def __unicode__(self):
        return unicode(self.nome) + ' ' + \
            '(' + unicode(self.curso) + ')'
    # unicode(self.curso) + '- ' + 

    class Meta:
        verbose_name_plural = "unidades curriculares"
        pass

    pass


class Ano(models.Model):
    ano = models.CharField(max_length = 120)
    estado = models.IntegerField(null = True)
    
    def __unicode__(self):
        return unicode(self.ano)

class DepartamentoAno(models.Model):
    ano = models.ForeignKey('Ano',
                            null = True,
                            blank = True
                            )
    departamento = models.ForeignKey('Departamento')
    
    def __unicode__(self):
        return unicode(self.departamento.nome)


class CursosAno(models.Model):
    ano = models.ForeignKey('Ano',
                            null = True,
                            blank = True
                            )
    curso = models.ForeignKey('Curso')
    
    def __unicode__(self):
        return unicode(self.curso.nome)


class UC_Ano(models.Model):
    unidadeCurricular = models.ForeignKey('UnidadeCurricular',
                                          null = True,
                                          blank = True
                                          )
    cursosAno = models.ForeignKey('CursosAno')
    
    def __unicode__(self):
        return unicode(self.unidadeCurricular.nome)
    


class Reducao(models.Model):
    '''
    cargos e outros tipos de redução
    '''
    nome = models.CharField(max_length = 120, unique = True)
    horas = models.IntegerField(default = 0, null = True)

    data_modificacao = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return unicode(self.nome)

    class Meta:
        verbose_name_plural = "reduções"

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

    nome = models.CharField(max_length = 100,
                            unique = True,
                            choices = TITULO_CHOICES)
    def __unicode__(self):
        return unicode(self.nome) 

    pass

class CursoDocente(models.Model):
    '''
    curso do docente
    junção de cursos de docentes
    '''
    docente = models.ForeignKey('Docente')
    titulo = models.ForeignKey('Titulo')
    curso = models.CharField(max_length = 200)
    instituicao = models.CharField(max_length = 200)
    cnaef = models.ForeignKey('Cnaef')

    def __unicode__(self):
        return unicode(self.docente) + '- ' + \
            unicode(self.titulo) + ' ' + \
            unicode(self.curso)

    class Meta:
        verbose_name_plural = "formação dos docentes"

    pass


class Docente(models.Model):
    '''
    caraterização de docente
    '''
    nome_completo = models.CharField(max_length = 300,
                                         unique = True)
                                         
    
    departamento = models.ForeignKey('Departamento')

    # escalao de vencimento do docente
    escalao = models.IntegerField(default = 100,
                                            blank = True,
                                            null = True,
                                            help_text = u"escalão de vencimento")

    regime_exclusividade = models.BooleanField(default = True)

    email = models.EmailField(blank = True, null = True, default = '')
    
    abreviatura = models.CharField(max_length = 120,
                                         unique = True,
                                         blank = True,
                                         null = True,
                                         default = " ")

    # foto = models.ImageField(height_field=250, 
    #                          width_field=200,
    #                          upload_to='fotos',
    #                          blank=True, null=True, default='')

    def __unicode__(self):
        return unicode(self.nome_completo)
    pass


class DocenteLogs(models.Model):
                                         
    docente = models.ForeignKey('Docente')

    # escalao de vencimento do docente
    id_user = models.IntegerField(default = 100,
                                            blank = True,
                                            null = True,
                                            help_text = u"identificação User")

    
    data_modificacao = models.DateTimeField(auto_now = True)


    def __unicode__(self):
        return unicode(self.id_user) + "" + unicode(self.data_modificacao)

    pass

class Contrato(models.Model):
    '''
    contrato realizado com um docente
    nomeadamente em mudanças de categoria
    '''
    docente = models.ForeignKey('Docente')

    categoria = models.ForeignKey('Categoria')
    percentagem = models.IntegerField(default = 100,
                                      blank = True,
                                      null = True,
                                      help_text = u'percentagem de tempo em que está contratado')
    tipo_contrato = models.ForeignKey('TipoContrato')

    data_inicio = models.DateField(null = True,
                                   default = datetime.\
                                       date(year = 1980,
                                            month = 1,
                                            day = 1))
    data_fim = models.DateField(null = True,
                                default = datetime.\
                                    date(year = 2050,
                                         month = 1,
                                         day = 1))

    data_modificacao = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return unicode(self.docente)

    pass

class TipoAula(models.Model):
    '''
    tipos de leccionacao de aulas
    '''
    TIPOS_CHOICES = (
        ('PL', u'Prática Laboratório'),
        ('TP', u'Teórico Prática'),
        ('T', u'Teórica'),
        ('TC', u'Trabalho Campo'),
        ('E', u'Estágio'),
        ('OT', u'Orientação Tutória'),
        ('S', u'Seminário'),
        ('O', u'Orientação'),
        )


    tipo = models.CharField(max_length = 30, choices = TIPOS_CHOICES)
    
    def __unicode__(self):
        return unicode(self.tipo)

    pass

class Turma(models.Model):
    '''
    Turma
    representa os semestres ativos de um curso
    num determinado ano letivo

    apenas podem ser criadas turmas para os
    cursos em atividade

    uma turma corresponde a um curso ativo
    e indica o número de alunos que frequentam a turma
    '''
    ANO_CHOICES = (
        (2013, u'2013'),
        (2014, u'2014'),
        (2015, u'2015'),
        (2016, u'2016'),
        (2017, u'2017'),
        (2018, u'2018'),
        (2019, u'2019'),
        (2020, u'2020'),
        (2021, u'2021'),
        (2022, u'2022'),
        )

    SEMESTRE_CHOICES = (
        (1, u'1'),
        (2, u'2'),
        (3, u'3'),
        (4, u'4'),
        (5, u'5'),
        (6, u'6'),
        (7, u'7'),
        (8, u'8'),
        (9, u'9'),
        (10, u'10'),
        )
    TURNO_CHOICES = (
        ('A', u'A'),
        ('B', u'B'),
        ('C', u'C'),
        ('D', u'D'),
        ('E', u'E'),
        ('F', u'F'),
        ('G', u'G'),
        ('H', u'H'),
        ('I', u'I'),
        )


    ano = models.IntegerField(choices = ANO_CHOICES)
    turno = models.CharField(max_length = 2,
                             choices = TURNO_CHOICES)
    numero_alunos = models.IntegerField(default = 20,
                                        null = True,
                                        blank = True)
    unidade_curricular = models.ForeignKey('UnidadeCurricular')
    
    # tipo de turma 
    tipo_aula = models.ForeignKey('TipoAula')
    
    # número de horas leccionadas
    horas = models.IntegerField(default = 0)

    observacoes = models.TextField(max_length = 500,
                                   null = True,
                                   blank = True,
                                   default = '',
                                   help_text = u'informação relevante')
    
    observacoesDirEscola = models.TextField(max_length = 500,
                                   null = True,
                                   blank = True,
                                   default = '',
                                   help_text = u'Fundamentação Turmas (Director de Escola)')
    
    observacoesDirDepartamento = models.TextField(max_length = 500,
                                   null = True,
                                   blank = True,
                                   default = '',
                                   help_text = u'OBSERVAÇÕES Director de Departamento')
    
    observacoesPresidencia = models.TextField(max_length = 500,
                                   null = True,
                                   blank = True,
                                   default = '',
                                   help_text = u'OBSERVAÇÕES Presidência')
    
    
    ucAno = models.ForeignKey('UC_Ano')


    def __unicode__(self):
        return unicode(self.unidade_curricular) + '- ' + \
            unicode(self.turno) + ', ' + unicode(self.tipo_aula) + \
            ' ' + unicode(self.ano)


    pass


class Modulos(models.Model):
    '''
    Modulos das turmas
    '''

    servico_docente = models.ForeignKey('ServicoDocente',
                                null = True,
                                blank = True)
    horas = models.IntegerField(default = 0)
    docente = models.ForeignKey('Docente',
                                null = True,
                                blank = True)
    
    departamento = models.ForeignKey('Departamento',
                                    null = True,
                                    blank = True)
    
    aprovacao = models.IntegerField(default = 0,
                                      blank = True,
                                      null = True,
                                      help_text = u'Aprovar se o modulo pode ser atribuido a outro departamento')
    
    def __unicode__(self):
        return unicode(self.servico_docente) + " " + unicode(self.docente) + " horas = " + unicode(self.horas)
        pass
    
    pass

class ServicoDocente(models.Model):
    '''
    ServicoDocente
    representação da atribuição de um serviço docente a 
    um determinado docente
    
    o serviço docente é referido apenas a serviço letivo
    '''
    turma = models.ForeignKey('Turma')
    # docente = models.ForeignKey('Docente',
    #                            null=True,
    #                            blank=True)
    horas = models.IntegerField(default = 0)
    
    def __unicode__(self):
        return unicode(self.turma) + ' ' + unicode(self.horas) + 'h'
    '''
    def __unicode__(self):
        return unicode(self.turma) + ' ' + \
            unicode(self.docente) + '= ' + unicode(self.horas) + 'h'
    '''
    class Meta:
        verbose_name_plural = "serviços docentes"
        pass
    pass


class ReducaoServicoDocente(models.Model):
    '''
    representação concreta de uma redução de serviço
    docente
    '''
    docente = models.ForeignKey('Docente')
    reducao = models.ForeignKey('Reducao')
    observacoes = models.TextField(max_length = 500,
                                   null = True,
                                   blank = True,
                                   default = '',
                                   help_text = u'colocar a justificação')

    data_inicio = models.DateField(null = True,
                                   default = datetime.\
                                       date(year = 2012,
                                            month = 1,
                                            day = 1))
    data_fim = models.DateField(null = True,
                                default = datetime.\
                                    date(year = 2013,
                                         month = 1,
                                         day = 1))

    data_modificacao = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return unicode(self.docente)

    class Meta:
        verbose_name_plural = "reduções serviço docente"
        pass

    pass
