#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
autor: José Jasnau Caeiro
data: 7 de junho de 2012
obs:
   permite carregar os docentes para a base de dados
'''

import csv
import sqlite3
from operator import itemgetter, attrgetter

UC    = 9
CURSO = 6
DEP   = 10
CNAEF = 11
ECTS  = 12
ANO   = 13
SEM   = 14
EUC   = 15
HLT   = 26
HLTP  = 27
HLPL  = 28
HLTC  = 29
HLS   = 30
HLE   = 31
HLOT  = 34
HLO   = 35
HRSD  = 17 # horas de redução de SD
ND    = 2  # nome do docente
CAT   = 4  # categoria
PER   = 5  # percentagem

# índices na folha de cálculo
IDX_UC    = 0 # Unidade Curricular
IDX_CURSO = 1 # Curso
IDX_DEP   = 2 # Departamento
IDX_CNAEF = 3 # CNAEF
IDX_ECTS  = 4 # ECTS
IDX_ANO   = 5 # ANO
IDX_SEM   = 6 # SEM
IDX_EUC   = 7 # 
IDX_HLT   = 8 # Horas Lei Teóricas
IDX_HLTP  = 9 # Horas Lei Teórico-Práticas
IDX_HLPL  = 10 # Horas Lei Prática-Laboratorial
IDX_HLTC  = 11 # Horas Lei 
IDX_HLS   = 12
IDX_HLE   = 13
IDX_HLOT  = 14
IDX_HLO   = 15
IDX_HRSD  = 16 # Horas de Redução de Serviço Docente
IDX_ND    = 17 # Nome do Docente
IDX_CAT    = 18 # Categoria
IDX_PER    = 19 # Percentagem

categorias = dict()

categorias[u'PROF ADJ'] = u'professor adjunto'
categorias[u'EQ ASS 1.º T'] = u'assistente do primeiro triénio'
categorias[u'ASS 2.º T'] = u'assistente do segundo triénio'
categorias[u'EQ ASS 1.º T'] = u'assistente do primeiro triénio'
categorias[u'EQ ASS 2.º T'] = u'assistente do segundo triénio'
categorias[u'PROF COORD'] = u'professor coordenador'
categorias[u'EQ PROF ADJ'] = u'professor adjunto'
categorias[u'PROF ADJ CONV'] = u'professor adjunto'
categorias[u'ASS CONV'] = u'assistente'
categorias[u'C EXTERNO'] = u'colaborador externo'
categorias[u'PROF REQ'] = u'colaborador externo'
categorias[u'PRELETOR'] = u'preletor'

def unique(items):
    found = set()
    keep = []
    add = found.add
    app = keep.append

    # apenas se adiciona o que não existe no par formado 
    # pelos dois primeiros itens
    
    for item in items:
        #if not( item[0] ==  '- - - - -'):
        par = item[0], item[1], item[IDX_ND]
        if par not in found:
            add(par)
            app(item)
    return keep

def unidades_unique(items):
    found = set()
    keep = []
    add = found.add
    app = keep.append

    # apenas se adiciona o que não existe no par formado 
    # pelos dois primeiros itens
    
    for item in items:
        #if not( item[0] ==  '- - - - -'):
        par = item[IDX_UC], item[IDX_CURSO]
        if par not in found:
            add(par)
            app(item)
    return keep

def cursos_unicos(items):
    found = set()
    keep = []
    add = found.add
    app = keep.append
    
    for item in items:
        par = item[1]
        if par not in found:
            add(par)
            app(item)
    return keep

def leitura_csv():
    '''
    leitura do ficheiro csv
    '''
    
    nome_ficheiro = "DSD1213Proposta360Dep30Mai12.csv"
    ficheiro = open(nome_ficheiro, 'rb')
    leitor = csv.reader(ficheiro,delimiter=',')
    lista = []
    for linha in leitor:
        if linha[CURSO]:
            lista.append( (linha[UC], 
                           linha[CURSO],
                           linha[DEP], 
                           linha[CNAEF], 
                           linha[ECTS], 
                           linha[ANO],
                           linha[SEM], 
                           linha[EUC], 
                           linha[HLT], 
                           linha[HLTP],
                           linha[HLPL], 
                           linha[HLTC], 
                           linha[HLS], 
                           linha[HLE],
                           linha[HLOT], 
                           linha[HLO], 
                           linha[HRSD], 
                           linha[ND],
                           linha[CAT],
                           linha[PER]))
            # print linha
        pass

    ficheiro.close()

    nova = unique(lista)
    
    #for item in nova:
    #    print item[0], len(item[0].rstrip()), ' ', item[1], ' ', item[2]
    return nova
    pass


def pesquisa_curso(nome_curso, cursor):
    t = (nome_curso,)
    cursor.execute('''SELECT id FROM distro_curso WHERE
                      nome =?''', t)
    res = cursor.fetchone()
    if res:
        return res[0]
    else:
        return None

def pesquisa_departamento(nome_dep, cursor):
    t = (nome_dep,)
    cursor.execute('''SELECT id FROM distro_departamento WHERE
                      nome =?''', t)

    res = cursor.fetchone()
    if res:
        return res[0]
    else:
        return None


def pesquisa_cnaef(cnaef, cursor):
    t = (cnaef,)
    cursor.execute('''SELECT id FROM distro_cnaef WHERE
                      codigo =?''', t)
    res = cursor.fetchone()
    if res:
        return res[0]
    else:
        return None

def pesquisa_categoria(categoria, cursor):
    t = (categoria,)
    cursor.execute('''SELECT id FROM distro_categoria WHERE
                      nome =?''', t)
    res = cursor.fetchone()
    if res:
        return res[0]
    else:
        return None

def pesquisa_epoca(epoca, cursor):
    t = (epoca,)
    cursor.execute('''SELECT id FROM distro_epoca WHERE
                      abreviatura =?''', t)
    res = cursor.fetchone()
    if res:
        return res[0]
    else:
        return None

def escrever_reducoes(ficheiro, unidades):
    # geração do ficheiro yaml com as unidades curriculares todas
    fich_yaml = open(ficheiro, "w")
    pk = 1
    for unidade in unidades:
        uc = unidade[IDX_UC]
        horas = unidade[IDX_HRSD]
        nome_curso = unicode(unidade[IDX_CURSO], 'utf-8')

        if nome_curso == u"Redução SD":
            # print pk, nome_curso, uc, horas

            fich_yaml.write("- model: distro.reducao\n")
            fich_yaml.write("  pk: {}\n".format(str(pk)))
            fich_yaml.write("  fields:\n")
            fich_yaml.write("    nome: {}\n".format(uc.replace(':','-')))
            fich_yaml.write("    horas: {}\n".format(horas.replace(':','-')))

            pk += 1
            continue

        pass

    fich_yaml.close()
    pass
    
def escrever_unidades_curriculares(ficheiro, unidades, cursor):
    # geração do ficheiro yaml com as unidades curriculares todas
    fich_yaml = open(ficheiro, "w")
    pk = 1
    for unidade in unidades:
        uc = unidade[IDX_UC]

        nome_curso = unicode(unidade[IDX_CURSO], 'utf-8')
        id_curso = pesquisa_curso(nome_curso, cursor)
        if not id_curso:
            if nome_curso == u"Redução SD":
                # print nome_curso, uc, " NONE"
                pass
            continue
        # print id_curso, nome_curso

        nome_departamento = unicode(unidade[IDX_DEP], 'utf-8')
        id_dep = pesquisa_departamento(nome_departamento, cursor)
        if not id_dep:
            print uc, ' ', nome_departamento, "DEP"
            pass

        cnaef = unidade[IDX_CNAEF]
        id_cnaef = pesquisa_cnaef(cnaef, cursor)
        # print id_cnaef, cnaef

        epoca = unidade[IDX_EUC]
        id_epoca = pesquisa_epoca(epoca, cursor)
        # print id_epoca, epoca

    
        fich_yaml.write("- model: distro.unidadecurricular\n")
        fich_yaml.write("  pk: {}\n".format(str(pk)))
        fich_yaml.write("  fields:\n")
        fich_yaml.write("    nome: {}\n".format(uc.replace(':','-')))

        if id_curso:
            fich_yaml.write("    curso: {}\n".format(id_curso))
        else:
            fich_yaml.write("    curso:\n")
            pass
        
        if id_dep:
            fich_yaml.write("    departamento: {}\n".format(id_dep))
        else:
            fich_yaml.write("    departamento:\n")        
            pass
        
        if id_cnaef:
            fich_yaml.write("    cnaef: {}\n".format(id_cnaef))
        else:
            fich_yaml.write("    cnaef:\n")
            pass
        
        fich_yaml.write("    ects: {}\n".\
                            format(unidade[IDX_ECTS].replace(',', '.')))
        fich_yaml.write("    ano: {}\n".\
                            format(unidade[IDX_ANO].replace('- - - - -', '1')))
        fich_yaml.write("    semestre: {}\n".\
                            format(unidade[IDX_SEM].replace('- - - - -','1')))
        if id_epoca:
            fich_yaml.write("    epoca: {}\n".format(id_epoca))
        else:
            fich_yaml.write("    epoca:\n")
            pass
        
        fich_yaml.write("    horas_lei_t: {}\n".\
                            format(unidade[IDX_HLT].replace(',', '.')))
        fich_yaml.write("    horas_lei_tp: {}\n".\
                            format(unidade[IDX_HLTP].replace(',', '.')))
        fich_yaml.write("    horas_lei_pl: {}\n".\
                            format(unidade[IDX_HLPL].replace(',', '.')))
        fich_yaml.write("    horas_lei_tc: {}\n".\
                            format(unidade[IDX_HLTC].replace(',', '.')))
        fich_yaml.write("    horas_lei_s: {}\n".\
                            format(unidade[IDX_HLS].replace(',', '.')))
        fich_yaml.write("    horas_lei_e: {}\n".\
                            format(unidade[IDX_HLE].replace(',', '.')))
        fich_yaml.write("    horas_lei_ot: {}\n".\
                            format(unidade[IDX_HLOT].replace(',', '.')))
        fich_yaml.write("    horas_lei_o: {}\n".\
                            format(unidade[IDX_HLO].replace(',', '.')))
        pk += 1
        pass

    fich_yaml.close()
    pass

def docentes_unicos(items):
    found = set()
    keep = []
    add = found.add
    app = keep.append
    
    for item in items:
        par = item[IDX_ND]

        if par not in found:
            add(par)
            app(item)
    return keep

def nome_docente_predicate(nome_docente):
    if nome_docente == ' ' or \
            nome_docente == 'a contratar' or \
            nome_docente == 'ECSC' or \
            nome_docente == 'CET - AHD' or \
            nome_docente == "ERASMUS - AHD" or \
            nome_docente == 'CET - CE' or \
            nome_docente == 'Docente A (Direito)' or \
            nome_docente == 'Docente B (Direito)' or \
            nome_docente == 'Docente C (Direito)' or \
            nome_docente == 'Docente D (Direito)' or \
            nome_docente == 'Docente E (Direito)' or \
            nome_docente == 'Docente Seminário' or \
            nome_docente == 'Antropólogo/Sociólogo a contratar' or \
            nome_docente == 'A contratar_2_EC_EnfMedicaor' or \
            nome_docente == 'Assistente social a contratar' or \
            nome_docente == 'CET - ECSC' or \
            nome_docente == 'ECSC' or \
            nome_docente == 'Psicólogo a contratar' or \
            nome_docente == 'CET - ENG' or \
            nome_docente == 'Por atribuir' or \
            nome_docente == 'Professor Doutorado a Contratar' or \
            nome_docente == 'CET - MCF' or \
            nome_docente == 'MCF' or \
            nome_docente == 'A contratar' or \
            nome_docente == 'A contratar ' or \
            nome_docente == 'A contratar_1_EC_EnfCirurgica' or \
            nome_docente == 'A contratar_1_EC_EnfMedica' or \
            nome_docente == 'A contratar_1_EC_Fundamentos' or \
            nome_docente == 'A contratar_1_EC_Smaterna_SIJuvenil' or \
            nome_docente == 'A contratar_2_EC_EnfCirurgica' or \
            nome_docente == 'A contratar_2_EC_EnfMedica' or \
            nome_docente == 'A contratar_2_EC_Fundamentos' or \
            nome_docente == 'A contratar_2_EC_Smaterna_SIJuvenil' or \
            nome_docente == 'A contratar_2_Enf_Especialidades' or \
            nome_docente == 'A contratar_3_EC_EnfCirurgica' or \
            nome_docente == 'A contratar_3_EC_EnfMedica' or \
            nome_docente == 'A contratar_3_EC_Smaterna_SIJuvenil' or \
            nome_docente == 'A contratar_4_EC_EnfCirurgica' or \
            nome_docente == 'A contratar_4_EC_EnfMedica' or \
            nome_docente == 'A contratar_5_EC_EnfCirurgica' or \
            nome_docente == 'A contratar_5_EC_EnfMedica' or \
            nome_docente == 'Assistente Social a contratar' or \
            nome_docente == 'Docente F' or \
            nome_docente == 'A contratar_1_Enf_Especialidades' or \
            nome_docente == 'Convidados_2_Enf_Medica' or \
            nome_docente == 'Convidados_3_Enf_Medica' or \
            nome_docente == 'Convidados_Enf_ComII_IIICPLEEC' or \
            nome_docente == 'Convidados_Enf_Scomunitária' or \
            nome_docente == 'Convidados_Familia_IIICPLEEC' or \
            nome_docente == 'CET - SAUDE' or \
            nome_docente == 'Convidados_1_Enf_Medica' or \
            nome_docente == 'Convidados_Enf_Cirurgica' or \
            nome_docente == 'Convidados_Enf_Gerontologia' or \
            nome_docente == 'Docente A' or \
            nome_docente == 'Docente B' or \
            nome_docente == 'Docente C' or \
            nome_docente == 'Docente D' or \
            nome_docente == 'Docente E' or \
            nome_docente == 'CET - TCA' or \
            (nome_docente[0] == 'C' and nome_docente[1] == '_'):
        return True
    else:
        return False

def escrever_docente(ficheiro, unidades, cursor):
    fich_yaml = open(ficheiro, "w")

    # ordenar docentes alfabeticamente
    unidades_ordenadas = sorted(unidades, key=itemgetter(IDX_ND))
    pk = 1
    for linha in unidades_ordenadas:
        nome_docente = linha[IDX_ND]

        departamento = unicode(linha[IDX_DEP], 'utf-8')
        id_dep = pesquisa_departamento(departamento, 
                                       cursor)
        categoria    = unicode(linha[IDX_CAT], 'utf-8')
        if categoria == ' - - - - -' or \
                categoria == u'#N/D' or \
                categoria == u'':
            continue
        cat = categorias[categoria]

        id_categoria = pesquisa_categoria(cat,
                                          cursor)

        # percentagem de tempo
        percentagem = linha[IDX_PER]

        if nome_docente_predicate(nome_docente):
            continue

        if categoria[0] == 'E' or \
                categoria[-1] == 'V' or \
                categoria[-1] == 'O':
            contrato = 3
        elif categoria[-1] == 'Q':
            contrato = 1
        elif categoria[-1] == 'R':
            # print 'R', nome_docente
            contrato = 5
        else:
            contrato = 2

        fich_yaml.write("- model: distro.docente\n")
        fich_yaml.write("  pk: {}\n".format(str(pk)))
        fich_yaml.write("  fields:\n")
        fich_yaml.write("    nome_completo: {0}\n".\
                            format(nome_docente))
        fich_yaml.write("    departamento: {0}\n".\
                            format(id_dep))
        fich_yaml.write("    categoria: {0}\n".\
                            format(id_categoria))
        fich_yaml.write("    tipo_contrato: {0}\n".\
                            format(contrato))

        # print pk, " ", nome_docente, "-", \
        #     linha[IDX_DEP], linha[IDX_CAT], id_dep, percentagem
        # print "    ", id_categoria, cat.encode('ascii', 'replace')
        
        pk += 1
        pass
    fich_yaml.close()
    pass

# leitura das unidades curriculares
unidades = leitura_csv()

conn = sqlite3.connect("../ipbeja.sqlite3")
cursor = conn.cursor()

unidades.pop(0)
print len(unidades)
cursos   = cursos_unicos(unidades)
print len(unidades)

docentes = docentes_unicos(unidades)
print len(unidades)

# tem de se pesquisar para cada unidade curricular
# o id do curso, o id do departamento, o id da área cnaef
# e o id da época

ficheiro_unidades_curriculares = "unidadecurricular.yaml"
unidades_unicas = unidades_unique(unidades)
print len(unidades_unicas)
escrever_unidades_curriculares(ficheiro_unidades_curriculares, 
                               unidades_unicas,
                               cursor)

ficheiro_reducoes = "reducoes.yaml"
escrever_reducoes(ficheiro_reducoes, unidades)

ficheiro_docentes = "docentes.yaml"
escrever_docente(ficheiro_docentes, docentes, cursor)

cursor.close()
