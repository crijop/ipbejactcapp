# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Reducoes.abreviatura'
        db.add_column('distro_reducoes', 'abreviatura', self.gf('django.db.models.fields.CharField')(default='', max_length=6), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Reducoes.abreviatura'
        db.delete_column('distro_reducoes', 'abreviatura')


    models = {
        'distro.categoria': {
            'Meta': {'object_name': 'Categoria'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'distro.cnaef': {
            'Meta': {'object_name': 'Cnaef'},
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '120', 'null': 'True', 'blank': 'True'})
        },
        'distro.curso': {
            'Meta': {'object_name': 'Curso'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'tipo_curso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.TipoCurso']"})
        },
        'distro.departamento': {
            'Meta': {'object_name': 'Departamento'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'sede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.UnidadeOrganica']"})
        },
        'distro.epoca': {
            'Meta': {'object_name': 'Epoca'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'distro.reducoes': {
            'Meta': {'object_name': 'Reducoes'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '6'}),
            'data_modificacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'distro.tipocontrato': {
            'Meta': {'object_name': 'TipoContrato'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'distro.tipocurso': {
            'Meta': {'object_name': 'TipoCurso'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'distro.unidadecurricular': {
            'Meta': {'object_name': 'UnidadeCurricular'},
            'ano': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'cnaef': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Cnaef']", 'null': 'True'}),
            'curso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Curso']"}),
            'data_modificacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Departamento']"}),
            'ects': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'epoca': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Epoca']"}),
            'horas_lei_e': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'horas_lei_o': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'horas_lei_ot': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'horas_lei_pl': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'horas_lei_s': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'horas_lei_t': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'horas_lei_tc': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'horas_lei_tp': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'semestre': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'})
        },
        'distro.unidadeorganica': {
            'Meta': {'object_name': 'UnidadeOrganica'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['distro']
