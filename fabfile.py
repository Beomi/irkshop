from fabric.contrib.files import append, exists, sed, put
from fabric.api import env, local, run, sudo
import random
import os
import json

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(PROJECT_DIR, "deploy.json")) as f:
    envs = json.loads(f.read())

def get_env(setting, envs):
    return envs[setting]

# TODO: Required Fields: REPO_URL, PROJECT_NAME, REMOTE_HOST, REMOTE_PASSWORD, REMOTE_USER @ deploy.json

# developer: chagne this!
REPO_URL = get_env('REPO_URL', envs)
PROJECT_NAME = get_env('PROJECT_NAME', envs)
REMOTE_HOST = get_env('REMOTE_HOST', envs)
STATIC_ROOT_NAME = 'static_deploy'
STATIC_URL_NAME = 'static'
MEDIA_ROOT = 'uploads'

# TODO: Server Engineer: you should add env.user as sudo user and NOT be root
env.user = get_env('REMOTE_USER', envs)
username = env.user
# Option: env.password
env.hosts = [
    get_env('REMOTE_HOST_SSH', envs),
    ]
env.password = get_env('REMOTE_PASSWORD', envs)
project_folder = '/home/{}/{}'.format(env.user, PROJECT_NAME)
apt_requirements = [
    'curl',
    'git',
    'python3-dev',
    'python3-pip',
    'build-essential',
    'libpq-dev',
    'postgresql',
    'postgresql-contrib',
    'apache2',
    'libapache2-mod-wsgi-py3',
    'python3-setuptools',
    'libssl-dev',
    'libffi-dev',
]

def new_server():
    setup()
    deploy()

def setup():
    _get_latest_apt()
    _install_apt_requirements(apt_requirements)
    _make_virtualenv()
    #_ufw_allow()

def deploy():
    _get_latest_source()
    _put_envs()
    _update_settings()
    _update_virtualenv()
    _update_static_files()
    _update_database()
    #_ufw_allow()
    _make_virtualhost()
    _grant_apache2()
    _restart_apache2()

def migrate():
    _put_envs()
    _update_settings()
    _update_virtualenv()
    _update_static_files()
    _update_database()
    _make_virtualhost()
    _grant_apache2()
    _restart_apache2()

def _put_envs():
    put('envs.json', '~/{}/envs.json'.format(PROJECT_NAME))
    put('bank_envs.json', '~/{}/bank_envs.json'.format(PROJECT_NAME))

def _get_latest_apt():
    update_or_not = input('would you update?: [y/n]')
    if update_or_not=='y':
        sudo('sudo apt-get update && sudo apt-get -y upgrade')

def _install_apt_requirements(apt_requirements):
    reqs = ''
    for req in apt_requirements:
        reqs += (' ' + req)
    sudo('sudo apt-get -y install {}'.format(reqs))

def _make_virtualenv():
    if not exists('~/.virtualenvs'):
        script = '''"# python virtualenv settings
                    export WORKON_HOME=~/.virtualenvs
                    export VIRTUALENVWRAPPER_PYTHON="$(command \which python3)"  # location of python3
                    source /usr/local/bin/virtualenvwrapper.sh"'''
        run('mkdir ~/.virtualenvs')
        sudo('sudo pip3 install virtualenv virtualenvwrapper')
        run('echo {} >> ~/.bashrc'.format(script))

def _get_latest_source():
    if exists(project_folder + '/.git'):
        run('cd %s && git fetch' % (project_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, project_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (project_folder, current_commit))

def _update_settings():
    settings_path = project_folder + '/{}/settings.py'.format(PROJECT_NAME)
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',
        'ALLOWED_HOSTS = ["%s"]' % (env.host,)
    )
    secret_key_file = project_folder + '/{}/secret_key.py'.format(PROJECT_NAME)
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv():
    virtualenv_folder = project_folder + '/../.virtualenvs/{}'.format(PROJECT_NAME)
    if not exists(virtualenv_folder + '/bin/pip'):
        run('cd /home/%s/.virtualenvs && virtualenv %s' % (env.user, PROJECT_NAME))
    run('%s/bin/pip install -r %s/requirements.txt' % (
        virtualenv_folder, project_folder
    ))

def _update_static_files():
    virtualenv_folder = project_folder + '/../.virtualenvs/{}'.format(PROJECT_NAME)
    run('cd %s && %s/bin/python3 manage.py collectstatic --noinput' % (
        project_folder, virtualenv_folder
    ))

def _update_database():
    virtualenv_folder = project_folder + '/../.virtualenvs/{}'.format(PROJECT_NAME)
    run('cd %s && %s/bin/python3 manage.py migrate --noinput' % (
        project_folder, virtualenv_folder
    ))

def _ufw_allow():
    sudo("ufw allow 'Apache Full'")
    sudo("ufw reload")

def _make_virtualhost():
    script = """'<VirtualHost *:80>
    ServerName {servername}
    Alias /{static_url} /home/{username}/{project_name}/{static_root}
    Alias /{media_url} /home/{username}/{project_name}/{media_url}
    <Directory /home/{username}/{project_name}/{media_url}>
        Require all granted
    </Directory>
    <Directory /home/{username}/{project_name}/{static_root}>
        Require all granted
    </Directory>
    <Directory /home/{username}/{project_name}/{project_name}>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    WSGIDaemonProcess {project_name} python-home=/home/{username}/.virtualenvs/{project_name} python-path=/home/{username}/{project_name}
    WSGIProcessGroup {project_name}
    WSGIScriptAlias / /home/{username}/{project_name}/{project_name}/wsgi.py
    ErrorLog ${{APACHE_LOG_DIR}}/error.log
    CustomLog ${{APACHE_LOG_DIR}}/access.log combined
    </VirtualHost>'""".format(
        static_root=STATIC_ROOT_NAME,
        username=env.user,
        project_name=PROJECT_NAME,
        static_url=STATIC_URL_NAME,
        servername=REMOTE_HOST,
        media_url=MEDIA_ROOT
    )
    sudo('echo {} > /etc/apache2/sites-available/{}.conf'.format(script, PROJECT_NAME))
    sudo('a2ensite {}.conf'.format(PROJECT_NAME))

def _grant_apache2():
    sudo('chown :www-data ~/{}'.format(PROJECT_NAME))
    # enable below if use sqlite3
    #sudo('chmod 775 ~/{}/db.sqlite3'.format(PROJECT_NAME))

def _restart_apache2():
    sudo('sudo service apache2 restart')