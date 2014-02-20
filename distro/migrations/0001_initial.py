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

        # Adding model 'UnidadeOrganica'
        db.create_table('distro_unidadeorganica', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('abreviatura', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal('distro', ['UnidadeOrganica'])

        # Adding model 'Departamento'
        db.create_table('distro_departamento', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('abreviatura', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('sede', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.UnidadeOrganica'])),
        ))
        db.send_create_signal('distro', ['Departamento'])

        # Adding model 'TipoCurso'
        db.create_table('distro_tipocurso', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('abreviatura', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal('distro', ['TipoCurso'])

        # Adding model 'Curso'
        db.create_table('distro_curso', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('abreviatura', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('tipo_curso', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.TipoCurso'])),
            ('semestre_letivos', self.gf('django.db.models.fields.IntegerField')(default=2)),
        ))
        db.send_create_signal('distro', ['Curso'])

        # Adding model 'Cnaef'
        db.create_table('distro_cnaef', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(default=' ', max_length=120, null=True, blank=True)),
            ('codigo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal('distro', ['Cnaef'])

        # Adding model 'GrauAcademico'
        db.create_table('distro_grauacademico', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('distro', ['GrauAcademico'])

        # Adding model 'Epoca'
        db.create_table('distro_epoca', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('abreviatura', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('distro', ['Epoca'])

        # Adding model 'UnidadeCurricular'
        db.create_table('distro_unidadecurricular', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('curso', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.Curso'])),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.Departamento'])),
            ('cnaef', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.Cnaef'], null=True)),
            ('ects', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('ano', self.gf('django.db.models.fields.IntegerField')(default=1, null=True)),
            ('semestre', self.gf('django.db.models.fields.IntegerField')(default=1, null=True)),
            ('epoca', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['distro.Epoca'], null=True)),
            ('horas_lei_t', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('horas_lei_tp', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('horas_lei_pl', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('horas_lei_tc', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('horas_lei_s', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('horas_lei_e', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('horas_lei_ot', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('horas_lei_o', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('data_modificacao', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('regente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.Docente'], null=True, blank=True)),
        ))
        db.send_create_signal('distro', ['UnidadeCurricular'])

        # Adding model 'Reducao'
        db.create_table('distro_reducao', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('horas', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('data_modificacao', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('distro', ['Reducao'])

        # Adding model 'Titulo'
        db.create_table('distro_titulo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('distro', ['Titulo'])

        # Adding model 'CursoDocente'
        db.create_table('distro_cursodocente', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.Docente'])),
            ('titulo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.Titulo'])),
            ('curso', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('instituicao', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('cnaef', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.Cnaef'])),
        ))
        db.send_create_signal('distro', ['CursoDocente'])

        # Adding model 'Docente'
        db.create_table('distro_docente', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome_completo', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.Departamento'])),
            ('categoria', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.Categoria'])),
            ('escalao', self.gf('django.db.models.fields.IntegerField')(default=100, null=True, blank=True)),
            ('percentagem', self.gf('django.db.models.fields.IntegerField')(default=100, null=True, blank=True)),
            ('tipo_contrato', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.TipoContrato'])),
            ('data_inicio', self.gf('django.db.models.fields.DateField')(default=datetime.date(1980, 1, 1), null=True)),
            ('data_fim', self.gf('django.db.models.fields.DateField')(default=datetime.date(2050, 1, 1), null=True)),
            ('data_modificacao', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('distro', ['Docente'])

        # Adding model 'TipoAula'
        db.create_table('distro_tipoaula', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('distro', ['TipoAula'])

        # Adding model 'Turma'
        db.create_table('distro_turma', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ano', self.gf('django.db.models.fields.IntegerField')()),
            ('turno', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('numero_alunos', self.gf('django.db.models.fields.IntegerField')(default=20, null=True, blank=True)),
            ('unidade_curricular', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.UnidadeCurricular'])),
            ('tipo_aula', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.TipoAula'])),
            ('horas', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('distro', ['Turma'])

        # Adding model 'ServicoDocente'
        db.create_table('distro_servicodocente', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('turma', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.Turma'])),
            ('docente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distro.Docente'], null=True, blank=True)),
            ('horas', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('distro', ['ServicoDocente'])


    def backwards(self, orm):
        
        # Deleting model 'TipoContrato'
        db.delete_table('distro_tipocontrato')

        # Deleting model 'Categoria'
        db.delete_table('distro_categoria')

        # Deleting model 'UnidadeOrganica'
        db.delete_table('distro_unidadeorganica')

        # Deleting model 'Departamento'
        db.delete_table('distro_departamento')

        # Deleting model 'TipoCurso'
        db.delete_table('distro_tipocurso')

        # Deleting model 'Curso'
        db.delete_table('distro_curso')

        # Deleting model 'Cnaef'
        db.delete_table('distro_cnaef')

        # Deleting model 'GrauAcademico'
        db.delete_table('distro_grauacademico')

        # Deleting model 'Epoca'
        db.delete_table('distro_epoca')

        # Deleting model 'UnidadeCurricular'
        db.delete_table('distro_unidadecurricular')

        # Deleting model 'Reducao'
        db.delete_table('distro_reducao')

        # Deleting model 'Titulo'
        db.delete_table('distro_titulo')

        # Deleting model 'CursoDocente'
        db.delete_table('distro_cursodocente')

        # Deleting model 'Docente'
        db.delete_table('distro_docente')

        # Deleting model 'TipoAula'
        db.delete_table('distro_tipoaula')

        # Deleting model 'Turma'
        db.delete_table('distro_turma')

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
            'escalao': ('django.db.models.fields.IntegerField', [], {'default': '100', 'null': 'True', 'blank': 'True'}),
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
            'horas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_alunos': ('django.db.models.fields.IntegerField', [], {'default': '20', 'null': 'True', 'blank': 'True'}),
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
            'regente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['distro.Docente']", 'null': 'True', 'blank': 'True'}),
            'semestre': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'})
        },
        'distro.unidadeorganica': {
            'Meta': {'object_name': 'UnidadeOrganica'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['distro']
