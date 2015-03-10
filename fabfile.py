# -*- coding: utf-8 -*-
"""
Fabric file used for uploading to the remote server.
"""
from datetime import datetime
from fabric.api import *
from fabric.contrib.project import rsync_project
from fabsettings import APP_NAME, APP_USER, PRODUCTION_HOST, SUDOER, REMOTE_TAR_DIR


env.hosts = [PRODUCTION_HOST]
env.name = 'production'
env.user = APP_USER


def _virtualenv(command):
    """
    Executes a command inside the remote virtualenv
    """
    with cd('src'):
        run('workon {0} && {0}'.format(APP_NAME, command))


def _manage_py(command):
    """
    Executes a django-admin.py command
    """
    _virtualenv('python manage.py {0}'.format(command))


def _clean_pyc():
    """
    Removes all .pyc files, to be used before tar.
    """
    local("find . -name '*.pyc' -exec rm {} \;")


def _create_tar(tar_name):
    """
    Creates a tarball of the local files
    """
    _clean_pyc()
    tar_files = ["app/", "bug_tracker/", "static/", "manage.py", "requirements.txt", "gunicorn_start"]
    local("tar zcf {0} {1}".format(tar_name, " ".join(tar_files)))


def _grunt_build():
    """
    Builds the local frontend
    """
    local('grunt build')


def _git_tag(tag_name):
    """
    Creates a tag and pushes
    """
    local('git tag {0}'.format(tag_name))
    local('git push origin {0}'.format(tag_name))


def _copy_tar(tar_name, remote_tar_name):
    """
    Copies the tar to the server
    :param tar_name:
    :param remote_tar_name:
    :return:
    """
    put(local_path=tar_name, remote_path=remote_tar_name)


def _delete_tar(tar_name, remote_tar_name):
    """
    Deletes the local tar.
    """
    local('unlink {0}'.format(tar_name))
    run('unlink {0}'.format(remote_tar_name))


def _unpack_tar(tar_name, tag_name):
    """
    Unpacks the tar on the remote server.
    """
    run('mkdir {0}/{1}/'.format(REMOTE_TAR_DIR, tag_name))
    run('tar zxf {0} -C {1}/{2}/'.format(tar_name, REMOTE_TAR_DIR, tag_name))
    run('unlink src')
    run('ln -s {0}/{1}/ src'.format(REMOTE_TAR_DIR, tag_name))


def _restart_service():
    """
    Restarts the gunicorn app
    """
    env.user = SUDOER
    run('sudo /usr/local/bin/supervisorctl restart {0}'.format(APP_NAME))
    env.user = APP_USER


def deploy():
    """
    Transfers the files to the remote server.
    """
    tag_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_") + env.name
    tar_name = '{0}.tar.gz'.format(tag_name)
    remote_tar_name = '{0}/{1}'.format(REMOTE_TAR_DIR, tar_name)

    _grunt_build()
    _git_tag(tag_name)
    _create_tar(tar_name)
    _copy_tar(tar_name, remote_tar_name)
    _unpack_tar(remote_tar_name, tag_name)
    _virtualenv('pip install -r requirements.txt --upgrade')
    _manage_py('collectstatic --noinput')
    _manage_py('migrate')
    _restart_service()
    _delete_tar(tar_name, remote_tar_name)


def push_media():
    """
    Pushes the dynamic media folder to the server.
    """
    rsync_project(remote_dir='.', local_dir='media', delete=True)


def pull_media():
    """
    Pushes the dynamic media folder to the server.
    """
    rsync_project(remote_dir='media', local_dir='.', upload=False, delete=True)
