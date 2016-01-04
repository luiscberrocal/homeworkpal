========================
homeworkpal_project
========================

This project follows best practices as espoused in `Two Scoops of Django: Best Practices for Django 1.6`_.

.. _`Two Scoops of Django: Best Practices for Django 1.6`: http://twoscoopspress.org/products/two-scoops-of-django-1-6

A project template for Django 1.6 (with a tag for Django 1.5).

To use this project follow these steps:

#. Create your working environment
#. Install Django
#. Create the new project using the django-two-scoops template
#. Install additional dependencies
#. Use the Django admin to create the project

*note: these instructions show creation of a project called "icecream".  You
should replace this name with the actual name of your project.*

Working Environment
===================

Windows
---------

::

	$ set DJANGO_SETTINGS_MODULE=homeworkpal_project.settings.local_acp

::

    $ celery -A homeworkpal_project worker -l info


Mac
------



::
  
    $ PATH=$PATH:/usr/local/sbin

    $ rabbitmq-server
::

    $ celery -A homeworkpal_project worker -l info



Dumping data to json
----------------------

::

  $ python manage.py dumpdata  --indent=4 --exclude auth.permission --exclude contenttypes > maximo/employees_fixtures.json




LDAP
------

Download pyldap-2.4.22-cp34-none-win32.whl from http://www.lfd.uci.edu/~gohlke/pythonlibs/

Install the whl file using the following command:

::

	> pip install C:\Users\lberrocal\Downloads\pyldap-2.4.22-cp34-none-win32.whl

The install the django-auth-ldap

::

	> pip install django-auth-ldap


Reference:

http://www.djm.org.uk/using-django-auth-ldap-active-directory-ldaps/

