all: 

migration:
	python manage.py schemamigration distro --auto
	python manage.py migrate distro

# carregamento de dados iniciais
initial:
	python manage.py loaddata categorias.yaml
	python manage.py loaddata unidadesorganicas.yaml
	python manage.py loaddata departamentos.yaml
	python manage.py loaddata tiposcursos.yaml
	python manage.py loaddata cursos.yaml

clean:
	rm ipbeja.sqlite3