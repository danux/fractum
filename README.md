# Fractum

Django based bug tracker. Instead of assigning a severity like critical or trivial, Fractum encourages users to order their bugs by priority.

Proof of concept only so far. Todo list includes ability to login. It's far from production ready. Includes a few tests.

[![Build Status](https://travis-ci.org/danux/fractum.svg?branch=master)](https://travis-ci.org/danux/fractum)


## Installation

Checkout the project. It's a pretty standard Django app. If you want the front end you'll need to use Grunt. It's just
bootstrap though, so do your own thing if you like.

    # Generate css, compress JS and move images to /static/
    $ grunt build

    # Watch files and auto-generate on change
    $ grunt dev

In terms of Django bits, do this.

    # Create a virtual env
    $ mkvirtualenv fractum

    # Install dependencies
    $ pip install -r requirements.txt

    # Create your own settings file, copy mine if you like (remember to change the secret key)
    $ cp app/settings_ddavies.py app/<your_settings>.py

    # Migrate the DB
    $ python manage.py migrate --settings=app.<your_settings>

    # Install fixtures to have a play
    $ python manage.py loaddata buckets statuses

    # Run the server
    $ python manage.py runserver_plus --settings=app.<your_settings>

* Change manage.py or symlink /settings.py to your settings to have shorter commands.
* I've also left my Fabric file in there. See below.


## Todo (in priority order)

* Re-order bucket interface
* User accounts
* Organisations
* Bucket permissions
* Non-Django admin control panel


## Fabric

The fabfile needs an accompanying fabsettings.py.

    APP_NAME = 'The name of the app (it assumes you store all your sites in /srv/sites/<APP_NAME/>'
    APP_USER = 'The user that owns the code'
    PRODUCTION_HOST = 'Your server'
    REMOTE_TAR_DIR = 'The path that the tarball is unpacked to. This deployment method keeps old copies for quick rollback'
    SUDOER = 'The sudo user that can restart the process. I use supervisord.'
