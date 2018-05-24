# Django with Jinja

## Set up Django Project
In bash:
```bash
mkdir django-jinja
cd django-jinja
virtualenv .env -p python3
source .env/bin/activate

pip install Django===2.0.5
pip install psycopg2
pip install jinja2
pip freeze > requirements.txt

django-admin startproject jinja_test
cd jinja_test

psql
jasontoups= CREATE DATABASE jinja_test;
jasontoups= CREATE USER jinjauser WITH PASSWORD 'beepbeep';
jasontoups= GRANT ALL PRIVILEGES ON DATABASE jinja_test TO jinjauser;
```

In settings.py, set up your database and app:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'jinja_test',
        'USER': 'jinjauser',
        'PASSWORD': 'beepbeep',
        'HOST': 'localhost'
    }
}
```

You can test this by running ```python manage.py runserver``` in bash and going to localhost:8000  

We have to set up a new app:
```bash
python manage.py startapp jinja
```
Add ```'jinja'``` to your list of installed apps in settings.py

In ```models.py```:
```python
from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    funds_raised = models.IntegerField()

    def __str__(self):
        return self.name
```

Now we migrate the model to the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

Next, we register the model to show up in our admin panel. Go to admin.py
```python
from django.contrib import admin
from .models import Candidate

admin.site.register(Candidate)
```

## Set up Jinja2
Make sure Jinja2 is installed and attached to requirements.txt  

In settings.py, change the template section:
```python
TEMPLATES = [
    # {
    #     'BACKEND': 'django.template.backends.django.DjangoTemplates',
    #     'DIRS': [],
    #     'APP_DIRS': True,
    #     'OPTIONS': {
    #         'context_processors': [
    #             'django.template.context_processors.debug',
    #             'django.template.context_processors.request',
    #             'django.contrib.auth.context_processors.auth',
    #             'django.contrib.messages.context_processors.messages',
    #         ],
    #     },
    # },
    # Keep this code if you want to 
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'templates/jinja2')],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'jinja_app.jinja2.Environment'
            # the first 'jinja' refers to the name of the app
        },
    },
]
```

Now we set up our views.py file in the app:
```python
from django.shortcuts import render
from .models import Candidate

def candidate_list(request):
    candidates = Candidate.objects.all()
    return render(request, 'jinja2/candidate_list.html', {'candidates': candidates})
```

And we set up the urls.py file in the same directory that has settings.py
```python
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jinja.urls'))
]
```

Now we create a ```urls.py``` file in the app directory:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.candidate_list, name='candidate_list')
]
```

Next, we have to create a jinja2.py file in our app:
```python
from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

def environment(**options):
    env = Environment(**options)
    env.globals.update({
       'static': staticfiles_storage.url,
       'url': reverse,
    })
    return env
```

Finally, we create a template in the directory ```templates/jinja2```. Let's call it ```candidate_list.html```
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Candidates</title>
</head>
<body>
  <h1>Candidates</h1>
  <ul>
    {% for item in candidates %}
      <li>
        {{candidate.name}}: {{candidate.funds_raised}}
      </li>
  </ul>
</body>
</html>
```