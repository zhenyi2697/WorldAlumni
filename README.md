# WorldAlumni - Find your schoolmates

## Lastest changes

03/15/2014: updated models for backend   

## Project Setup

WorldAlumni depends on the following packages:

1.MySQL:

Install MySQL from official site, or use homebrew (For Mac OS only):

	$ brew install mysql

Install MySQLWorkbench from official site for easier management.

2.Python packages:

[Django](https://www.djangoproject.com/): Framework

	$ pip install django

[MySQLdb](http://mysql-python.sourceforge.net/): Python interface for MySQL

	$ pip install mysql-python

[Django Grappelli](https://pypi.python.org/pypi/django-grappelli):

	$ sudo pip install django-grappelli

[Django south](http://south.readthedocs.org/en/latest/):
Since Django does not provide schema migration, to avoid manully modify the database schema, we use Django-south to automize this process.

	$ sudo pip install south

[Python social auth](http://psa.matiasaguirre.net/docs/index.html):   

    $ sudo pip install python-social-auth

[Django Rest Framework](http://www.django-rest-framework.org/):   
We use djangoRestFramework to develop our rest apis

    $ sudo pip install djangorestframework
    $ sudo pip install markdown
    $ sudo pip install django-filter

## Configure and sync database

Configure your WorldAlumni/settings.py to connect to your local mysql database:

	DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',   
        'NAME': 'worldalumni', 
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '', 
        'OPTIONS': {
            'charset': 'utf8',
            'use_unicode': True,
            'init_command': 'SET storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci',
        }
    }

Then, sync database:

	$ python manage.py syncdb

#### Trouble shooting using django-south:   
The first you do the schemamigration, there probably will be an error which said:

	django.db.utils.DatabaseError: table "myapp_tablename" already exists

You should specify the --fake option the first time we do migration:

	$ ./manage.py migrate myapp --fake
	
More details following this post: [http://stackoverflow.com/questions/3090648/django-south-table-already-exists](http://stackoverflow.com/questions/3090648/django-south-table-already-exists)

## Tutorials

[Setup Django and Mysql-Python on Mac OS Lion](http://decoding.wordpress.com/2012/01/23/how-to-setup-django-and-mysql-python-on-mac-os-x-lion/)

## Connect to social networks

We use [Python Social Authentication](http://psa.matiasaguirre.net/docs/index.html) for accesing user profile information.

Apply for a Facebook application and a LinkedIn one. The domain of the app is registered at http://worldalumni.io:8000/ during the developement. Change /etc/hosts to add this hostname to 127.0.0.1 to direct local visits.

Now: logging in for both networks is fine, but no information retrievement is not implemented. Integration with server db is not clear.
To do: grasp auth procedure and implement views and templates logically. Examples available on psa github page. 'User' concept in Django.

**Should change /etc/hosts and added this following entry into it **

    127.0.0.1 worldalumni.io



