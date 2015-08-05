Django contrib.auth compliant User model
========================================

- Decoupled email functionality
- Optional usernames
- More stuff

Usage
-----

Subclass the ``UUIDUser`` whereever you want to.

::
   from uuiduser import UUIDUser

   class User(UUIDUser):
     pass

Implement any custom behavior or fields you want to.

Add the following to your ``settings.py`` file.

::

   AUTH_USER_MODEL = 'my_user_app.User'


Commands (manage.py)
~~~~~~~~~~~~~~~~~~~~

When using the ``createsuperuser`` command, the first prompt will be for
``Uuid``.  You must enter a blank value for this.


Build
-----

Build a source distribution with:

::

   python setup.py sdist



Development
-----------

Project setup for development.

This may assume the existance of several system dependencies.  A short list
includes, but may not be limited to:

- python (2.7)
- virtualenv
- pip

For the most part, you should be able to copy/paste the below script... but I
make no promises.  I'll (likely) provide a build utility later.

::

   export PROJECT_ROOT="/path/to/project/root"

   cd $PROJECT_ROOT

   # Create and source a virtual environment
   virtualenv venv
   source venv/bin/activate

   # Install project requirements into virtualenv
   pip install -r requirements.txt
