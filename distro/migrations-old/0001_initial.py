# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TipoContrato'
        db.create_table('distro_tipocontrato', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('distro', ['TipoContrato'])

        # Adding model 'Categoria'
        db.create_table('distro_categoria', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('distro', ['Categoria'])


    def backwards(self, orm):
        
        # Deleting model 'TipoContrato'
        db.delete_table('distro_tipocontrato')

        # Deleting model 'Categoria'
        db.delete_table('distro_categoria')


    models = {
        'distro.categoria': {
            'Meta': {'object_name': 'Categoria'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'distro.tipocontrato': {
            'Meta': {'object_name': 'TipoContrato'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['distro']
