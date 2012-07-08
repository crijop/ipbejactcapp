# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Curso'
        db.create_table('distro_curso', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('abreviatura', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('tipo_curso', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.TipoCurso'])),
            ('codigo', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('distro', ['Curso'])


    def backwards(self, orm):
        
        # Deleting model 'Curso'
        db.delete_table('distro_curso')


    models = {
        'distro.categoria': {
            'Meta': {'object_name': 'Categoria'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'distro.curso': {
            'Meta': {'object_name': 'Curso'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'codigo': ('django.db.models.fields.IntegerField', [], {}),
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
        'distro.unidadeorganica': {
            'Meta': {'object_name': 'UnidadeOrganica'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['distro']
