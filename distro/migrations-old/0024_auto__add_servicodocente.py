# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ServicoDocente'
        db.create_table('distro_servicodocente', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('turma', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.Turma'])),
            ('docente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.Docente'])),
        ))
        db.send_create_signal('distro', ['ServicoDocente'])


    def backwards(self, orm):
        
        # Deleting model 'ServicoDocente'
        db.delete_table('distro_servicodocente')


    models = {
        'distro.categoria': {
            'Meta': {'object_name': 'Categoria'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'distro.cnaef': {
            'Meta': {'object_name': 'Cnaef'},
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
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
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'sede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.UnidadeOrganica']"})
        },
        'distro.docente': {
            'Meta': {'object_name': 'Docente'},
            'categoria': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Categoria']"}),
            'data_fim': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2050, 1, 1)', 'null': 'True'}),
            'data_inicio': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(1980, 1, 1)', 'null': 'True'}),
            'data_modificacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Departamento']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome_completo': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'percentagem': ('django.db.models.fields.IntegerField', [], {'default': '100', 'null': 'True', 'blank': 'True'}),
            'tipo_contrato': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.TipoContrato']"})
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
        'distro.servicodocente': {
            'Meta': {'object_name': 'ServicoDocente'},
            'docente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Docente']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'turma': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Turma']"})
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
        'distro.titulo': {
            'Meta': {'object_name': 'Titulo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'distro.turma': {
            'Meta': {'object_name': 'Turma'},
            'ano': ('django.db.models.fields.IntegerField', [], {}),
            'curso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Curso']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_alunos': ('django.db.models.fields.IntegerField', [], {'default': '20', 'null': 'True', 'blank': 'True'}),
            'semestre': ('django.db.models.fields.IntegerField', [], {}),
            'turno': ('django.db.models.fields.CharField', [], {'max_length': '2'})
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
