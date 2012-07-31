# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Categoria', fields ['nome']
        db.create_unique('distro_categoria', ['nome'])

        # Adding unique constraint on 'UnidadeOrganica', fields ['nome']
        db.create_unique('distro_unidadeorganica', ['nome'])

        # Adding unique constraint on 'UnidadeOrganica', fields ['abreviatura']
        db.create_unique('distro_unidadeorganica', ['abreviatura'])

        # Adding unique constraint on 'Departamento', fields ['nome']
        db.create_unique('distro_departamento', ['nome'])

        # Adding unique constraint on 'Departamento', fields ['abreviatura']
        db.create_unique('distro_departamento', ['abreviatura'])

        # Adding unique constraint on 'Docente', fields ['nome_completo']
        db.create_unique('distro_docente', ['nome_completo'])

        # Adding unique constraint on 'TipoCurso', fields ['nome']
        db.create_unique('distro_tipocurso', ['nome'])

        # Adding unique constraint on 'TipoCurso', fields ['abreviatura']
        db.create_unique('distro_tipocurso', ['abreviatura'])


    def backwards(self, orm):
        # Removing unique constraint on 'TipoCurso', fields ['abreviatura']
        db.delete_unique('distro_tipocurso', ['abreviatura'])

        # Removing unique constraint on 'TipoCurso', fields ['nome']
        db.delete_unique('distro_tipocurso', ['nome'])

        # Removing unique constraint on 'Docente', fields ['nome_completo']
        db.delete_unique('distro_docente', ['nome_completo'])

        # Removing unique constraint on 'Departamento', fields ['abreviatura']
        db.delete_unique('distro_departamento', ['abreviatura'])

        # Removing unique constraint on 'Departamento', fields ['nome']
        db.delete_unique('distro_departamento', ['nome'])

        # Removing unique constraint on 'UnidadeOrganica', fields ['abreviatura']
        db.delete_unique('distro_unidadeorganica', ['abreviatura'])

        # Removing unique constraint on 'UnidadeOrganica', fields ['nome']
        db.delete_unique('distro_unidadeorganica', ['nome'])

        # Removing unique constraint on 'Categoria', fields ['nome']
        db.delete_unique('distro_categoria', ['nome'])


    models = {
        'distro.categoria': {
            'Meta': {'object_name': 'Categoria'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'distro.cnaef': {
            'Meta': {'object_name': 'Cnaef'},
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '120', 'null': 'True', 'blank': 'True'})
        },
        'distro.contrato': {
            'Meta': {'object_name': 'Contrato'},
            'categoria': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Categoria']"}),
            'data_fim': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2050, 1, 1, 0, 0)', 'null': 'True'}),
            'data_inicio': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(1980, 1, 1, 0, 0)', 'null': 'True'}),
            'data_modificacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'docente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Docente']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentagem': ('django.db.models.fields.IntegerField', [], {'default': '100', 'null': 'True', 'blank': 'True'}),
            'tipo_contrato': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.TipoContrato']"})
        },
        'distro.curso': {
            'Meta': {'object_name': 'Curso'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'semestre_letivos': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'tipo_curso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.TipoCurso']"})
        },
        'distro.cursodocente': {
            'Meta': {'object_name': 'CursoDocente'},
            'cnaef': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Cnaef']"}),
            'curso': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'docente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Docente']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instituicao': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'titulo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Titulo']"})
        },
        'distro.departamento': {
            'Meta': {'object_name': 'Departamento'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'sede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.UnidadeOrganica']"})
        },
        'distro.docente': {
            'Meta': {'object_name': 'Docente'},
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Departamento']"}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'escalao': ('django.db.models.fields.IntegerField', [], {'default': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome_completo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '300'}),
            'regime_exclusividade': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'distro.epoca': {
            'Meta': {'object_name': 'Epoca'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'distro.grauacademico': {
            'Meta': {'object_name': 'GrauAcademico'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'distro.reducao': {
            'Meta': {'object_name': 'Reducao'},
            'data_modificacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'horas': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'})
        },
        'distro.reducaoservicodocente': {
            'Meta': {'object_name': 'ReducaoServicoDocente'},
            'data_fim': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 1, 0, 0)', 'null': 'True'}),
            'data_inicio': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 1, 1, 0, 0)', 'null': 'True'}),
            'data_modificacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'docente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Docente']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacoes': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'reducao': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Reducao']"})
        },
        'distro.servicodocente': {
            'Meta': {'object_name': 'ServicoDocente'},
            'docente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Docente']", 'null': 'True', 'blank': 'True'}),
            'horas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'turma': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Turma']"})
        },
        'distro.tipoaula': {
            'Meta': {'object_name': 'TipoAula'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'distro.tipocontrato': {
            'Meta': {'object_name': 'TipoContrato'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'distro.tipocurso': {
            'Meta': {'object_name': 'TipoCurso'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'distro.titulo': {
            'Meta': {'object_name': 'Titulo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'distro.turma': {
            'Meta': {'object_name': 'Turma'},
            'ano': ('django.db.models.fields.IntegerField', [], {}),
            'horas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_alunos': ('django.db.models.fields.IntegerField', [], {'default': '20', 'null': 'True', 'blank': 'True'}),
            'observacoes': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'tipo_aula': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.TipoAula']"}),
            'turno': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'unidade_curricular': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.UnidadeCurricular']"})
        },
        'distro.unidadecurricular': {
            'Meta': {'object_name': 'UnidadeCurricular'},
            'ano': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'cnaef': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Cnaef']", 'null': 'True'}),
            'curso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Curso']"}),
            'data_modificacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Departamento']"}),
            'ects': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'epoca': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['distro.Epoca']", 'null': 'True'}),
            'horas_lei_e': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'horas_lei_o': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'horas_lei_ot': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'horas_lei_pl': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'horas_lei_s': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'horas_lei_t': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'horas_lei_tc': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'horas_lei_tp': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'regente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Docente']", 'null': 'True', 'blank': 'True'}),
            'semestre': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'})
        },
        'distro.unidadeorganica': {
            'Meta': {'object_name': 'UnidadeOrganica'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        }
    }

    complete_apps = ['distro']