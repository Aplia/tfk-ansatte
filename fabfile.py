# coding=utf-8
import os
import shutil

import sys

from StringIO import StringIO
from fabric.api import env, cd
from fabric.colors import yellow, red, magenta, green
from fabric.context_managers import lcd, hide
from fabric.decorators import task
from fabric.operations import local, run, put
from fabric.utils import puts, abort
from fabric.contrib import files

env.forward_agent = True
env.branch = "master"


@task
def verify_remote_git_status():
    """
    Checks that the working copy of the remote is not modified.
    If it is it aborts the execution.
    """
    with cd(env.path):
        with hide('running', 'stdout'):
            status = run("git status --porcelain")
        if len(status) > 0:
            run("git status")
            abort(red("\nThe project's git status on the server is dirty.\n"
                      "Please ensure there are no uncommitted changes before continuing."))


@task
def update_git():
    """
    Updates git working copy by fetching the latest commits and merging them in
    if there are no merge commits needed.
    :return:
    """
    branch = env.branch
    with cd(env.path):
        run("git fetch -q")
        run("git checkout %s -q" % branch)
        # Often changes to this file that we don't need
        run("test -f .gitignore && git checkout .gitignore || true")
        run("git merge --ff-only origin/%s" % branch)
        if files.exists(os.path.join(env.path, ".gitmodules")):
            run("git submodule sync -q")
            run("git submodule update --init --recursive -q")


@task
def setup():
    if not os.path.exists('.env'):
        print("Creating initial " + yellow(".env"))
        shutil.copy('.env-dist', '.env')
    if not os.path.exists('backend/settings/.env'):
        print("Creating initial " + yellow("backend/settings/.env"))
        shutil.copy('backend/settings/.env-dist', 'backend/settings/.env')
    if not os.path.exists('backend/settings/local.py'):
        print("Creating initial " + yellow("backend/settings/local.py"))
        shutil.copy('backend/settings/local-dist.py', 'backend/settings/local.py')
    if not os.path.exists('backend/requirements/local.txt'):
        print("Creating initial " + yellow("backend/requirements/local.txt"))
        shutil.copy('backend/requirements/local-dist.txt', 'backend/requirements/local.txt')


@task
def changes():
    """ Shows list of commits that are not yet in production """
    branch = env.branch
    with cd(env.path):
        puts(u"Checking for changes in path {}".format(green(env.path)))
        run("git fetch -q")
        run("git log --stat %s..origin/%s" % (branch, branch))


@task
def diffchanges():
    """ Shows diff of changes that are not yet in production """
    branch = env.branch
    with cd(env.path):
        puts(u"Checking diff in path {}".format(green(env.path)))
        run("git fetch -q")
        run("git diff %s..origin/%s" % (branch, branch))


@task
def deploy():
    puts(u"Deploying in path {}".format(green(env.path)))
    verify_remote_git_status()
    update_git()

    with cd(env.path):
        # Store the git revision in .env-prod which will then be used by docker-compose
        git_rev = run("git rev-parse HEAD")
        git_rev_io = StringIO()
        git_rev_io.write("""
GIT_REV={git_rev}
""".format(git_rev=git_rev).replace("\r\n", "\n"))
        put(git_rev_io, ".env-prod")

        # Build the frontend first and use it for creating the ember assets files
        puts(yellow("Building frontend application"))
        run("docker-compose -f docker-compose.prod.yml build frontend")
        run("docker-compose -f docker-compose.prod.yml run --rm frontend ./build.sh")

        # Then build the backend-assets which allow for running collectstatic
        # and then gather the files in the backend/staticfiles folder
        puts(yellow("Building Django static files"))
        run("docker-compose -f docker-compose.prod.yml build backend-assets")
        run("docker-compose -f docker-compose.prod.yml run --rm -e DEPLOY_ENV=production backend-assets "
            "python manage.py collectstatic --no-input")

        puts(yellow("Building docker images with static files"))
        run("docker-compose -f docker-compose.prod.yml build")

        puts(yellow("Migrating database"))
        run("docker-compose -f docker-compose.prod.yml run --rm backend python manage.py migrate")

        puts(yellow("(Re)Starting services"))
        run("docker-compose -f docker-compose.prod.yml down")
        run("docker-compose -f docker-compose.prod.yml up -d rproxy backend postgres")
