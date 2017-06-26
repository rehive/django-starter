import os
import dotenv
import yaml
from io import BytesIO

from fabric.api import env, local, run, task, settings, abort, put, cd, prefix, get, sudo, shell_env, open_shell, prompt, lcd
from fabric.colors import red, green, yellow, white
from fabric.context_managers import hide
from fabric.contrib.project import rsync_project
import posixpath


def set_env(config, version_tag=None):
    """
    Fabric environmental variable setup
    """
    # Bug: when setting this inside a function. Using host_string as workaround
    config_dict = get_config(config)
    env.hosts = [config_dict['HOST_NAME'], ]
    env.host_string = config_dict['HOST_NAME']

    env.project_name = config_dict['PROJECT_NAME']
    env.project_dir = posixpath.join('/srv/images/', env.project_name)
    env.use_ssh_config = True

    env.image_name = config_dict['IMAGE'].split(':')[0]
    env.base_image_name = env.image_name + '_base'
    env.version_tag = version_tag

    env.env_file = config_dict['ENV_FILE']
    env.celery_id = config_dict['CELERY_ID']
    env.compose_project_name = config_dict['PROJECT_NAME']
    env.postgres_port = config_dict['POSTGRES_PORT']

    env.build_dir = '/srv/build'
    env.local_path = os.path.dirname(__file__)


def format_yaml(template, config):
    """Replace in ${ENV_VAR} in template with value"""
    formatted = template
    for k, v in config.items():
        formatted = formatted.replace('${%s}' % k, v)
    return formatted


def get_config(config):
    """Import config file as dictionary"""
    if config[-5:] != '.yaml':
        config += '.yaml'

    # Use /server as base path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    server_dir_path = dir_path
    if not os.path.isabs(config):
        config = os.path.join(server_dir_path, config)

    with open(config, 'r') as stream:
        config_dict = yaml.load(stream)

    return config_dict


def upload():
    """Upload entire project to server"""
    # Bug: when setting this inside a function. Using host_string as workaround
    run('mkdir -p /srv/images/'+env.project_name+'/')
    rsync_project(
        env.project_dir, './',
        exclude=(
            '.git', '.gitignore', '__pycache__', '*.pyc', '.DS_Store', 'environment.yml',
            'fabfile.py', 'Makefile', '.idea', 'bower_components', 'node_modules',
            '.env.example', 'README.md', 'var'
        ), delete=True)

# Wrapper Functions:


def docker(cmd='--help'):
    """
    Wrapper for docker
    """
    template = 'docker {cmd}'.format(cmd=cmd)
    run(template)


def compose(cmd='--help', version='latest'):
    """
    Wrapper for docker-compose
    """

    env_file = os.path.join(env.project_dir, env.env_file)

    env_vars = ("IMAGE_NAME={image_name} "
                "VERSION={version} "
                "ENV_FILE={env_file} "
                "CELERY_ID={celery_id}  "
                "COMPOSE_PROJECT_NAME={compose_project_name} "
                "POSTGRES_PORT={postgres_port} "
                ).format(image_name=env.image_name,
                         env_file=env_file,
                         celery_id=env.celery_id,
                         compose_project_name=env.compose_project_name,
                         postgres_port=env.postgres_port,
                         version=version)

    path = 'etc/compose/docker-compose.yml'

    with cd(env.project_dir):
        run('{env} docker-compose -f {path} {cmd}'.format(env=env_vars, cmd=cmd, path=path))

# App Image Builder:
def gcloud_login():
    """Authorise gcloud on server"""
    #  TODO: figure out service accounts
    with cd(env.project_dir):
        run('gcloud auth login')


def build():
    """
    Build project's docker image
    """
    image = '{}:{}'.format(env.image_name, env.version_tag)
    cmd = 'docker build -t {image} .'.format(image=image)
    with cd(env.project_dir):
        run(cmd)


def push():
    """
    Build, tag and push docker image
    """
    image = '{}:{}'.format(env.image_name, env.version_tag)
    build()
    with cd(env.project_dir):
        run('gcloud docker -- push %s' % image)

# Base Image Builder:
# No longer needed for Alpine build
# Kept this setup in case there are issues due to Alpine
def base():
    """Build and push base image"""
    wheels()
    build_base()
    push_base()


def wheels():
    """
    Remotely build python binaries on image-factory server
    """
    with lcd(env.local_path):
        put('./requirements.txt', '/srv/build/wheel_requirements.txt')
        put('./etc/base_image/image_requirements.txt',
            '/srv/build/requirements.txt')

    with cd('/srv/build/wheelhouse'):
        run('rm -rf *.whl')

    compose(cmd='-f service.yml -p %s run --rm wheel-factory' %
            env.project_name, path='/srv/build')


def build_base():
    """
    Remotely build base python image with all installed packages on image-factory server
    """
    with lcd(env.local_path):
        put('./requirements.txt', '/srv/build/requirements.txt')

    with cd('/srv/build'):
        run('docker build -t {base_image_name} .'.format(
            base_image_name=env.base_image_name,
        ))


def push_base():
    """
    Push base docker image
    """
    docker('login')
    docker('push %s' % env.base_image_name)
