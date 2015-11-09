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


::
  
    $ PATH=$PATH:/usr/local/sbin

    $ rabbitmq-server

::

    $ celery -A homeworkpal_project worker -l info



Dumping data to json
----------------------

::

  $ python manage.py dumpdata  --indent=4 --exclude auth.permission --exclude contenttypes > maximo/employees_fixtures.json


