server:
	python manage.py runserver
db:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver
shell:
	python manage.py shell