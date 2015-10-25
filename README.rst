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

You have several options in setting up your working environment.  We recommend
using virtualenv to separate the dependencies of your project from your system's
python environment.  If on Linux or Mac OS X, you can also use virtualenvwrapper to help manage multiple virtualenvs across different projects.

Virtualenv Only
---------------

First, make sure you are using virtualenv (http://www.virtualenv.org). Once
that's installed, create your virtualenv::

    $ virtualenv icecream

You will also need to ensure that the virtualenv has the project directory
added to the path. Adding the project directory will allow `django-admin.py` to
be able to change settings using the `--settings` flag.

Virtualenv with virtualenvwrapper
------------------------------------

In Linux and Mac OSX, you can install virtualenvwrapper (http://virtualenvwrapper.readthedocs.org/en/latest/),
which will take care of managing your virtual environments and adding the
project path to the `site-directory` for you::

    $ mkdir icecream
    $ mkvirtualenv -a icecream icecream-dev
    $ cd icecream && add2virtualenv `pwd`

Using virtualenvwrapper with Windows
----------------------------------------

There is a special version of virtualenvwrapper for use with Windows (https://pypi.python.org/pypi/virtualenvwrapper-win).::

    > mkdir icecream
    > mkvirtualenv icecream-dev
    > add2virtualenv icecream


Installing Django
=================

To install Django in the new virtual environment, run the following command::

    $ pip install django

Creating your project
=====================

To create a new Django project called '**icecream**' using
django-twoscoops-project, run the following command::

    $ django-admin.py startproject --template=https://github.com/twoscoops/django-twoscoops-project/archive/master.zip --extension=py,rst,html icecream_project

For Django 1.5 users, we recommend::

    $ django-admin.py startproject --template=https://github.com/twoscoops/django-twoscoops-project/archive/1.5.zip --extension=py,rst,html icecream_project

Installation of Dependencies
=============================

Depending on where you are installing dependencies:

In development::

    $ pip install -r requirements/local.txt

For production::

    $ pip install -r requirements.txt

*note: We install production requirements this way because many Platforms as a
Services expect a requirements.txt file in the root of projects.*

Running Commands
==================

::

  $ python manage.py load_employees C:\Users\lberrocal\PycharmProjects\homeworkpal\test_data\collaborator.xlsx --settings=homeworkpal_project.settings.local_acp

Follows Best Practices
======================

.. image:: http://twoscoops.smugmug.com/Two-Scoops-Press-Media-Kit/i-C8s5jkn/0/O/favicon-152.png
   :name: Two Scoops Logo
   :align: center
   :alt: Two Scoops of Django
   :target: http://twoscoopspress.org/products/two-scoops-of-django-1-6

This project follows best practices as espoused in `Two Scoops of Django: Best Practices for Django 1.6`_.

.. _`Two Scoops of Django: Best Practices for Django 1.6`: http://twoscoopspress.org/products/two-scoops-of-django-1-6

python manage.py dumpdata homework auth --indent 4 --natural-foreign --settings=homeworkpal_project.settings.local_acp


Versions
===========


0.1.1 :  Basic model with basic admin functions

0.2.0 :  Added a validator and a unique together constraint

0.2.1 :  Bug fixes on unique together

0.3.0 : Added fixtures, command to dumpdata

0.4.0 : Implemented ListView with Bootstrap CSS