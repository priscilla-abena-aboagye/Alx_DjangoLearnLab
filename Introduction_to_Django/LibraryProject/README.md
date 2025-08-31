# LibraryProject
A simple Django project created as a starting point for learning and building with Django.

- created an app 
```python
python manage.py startapp <name>
```
- created a model 
```python
title = models.CharField(max_length=200)
```
- made migrations
```python
python manage.py makemigrations
python manage.py migrate
```
- open the shell to interact with the database
```python 
python manage.py shell
```
- created a requirement.txt file
```python 
pip freeze > requirement.txt
```
- created a super user for the admin panel 
```python 
python manage.py createsuperuser
```

- registered the models 
```python
admin.site.register(Book)
```

