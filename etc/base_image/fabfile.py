import os
import dotenv

from fabric.api import env, local, run, task, settings, abort, put, cd, prefix, get, sudo, shell_env, open_shell, prompt, lcd
from fabric.colors import red, green, yellow, white
from fabric.context_managers import hide
from fabric.contrib.project import rsync_project

def set_env():
    """
    Fabric environmental variable setup
    """
    env.local_dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    dotenv.load_dotenv(env.local_dotenv_path)
    env.project_name = os.environ.get('PROJECT_NAME', '')
    env.use_ssh_config = True

    # Bug: when setting this inside a function. Using host_string as workaround
    env.hosts = [os.environ.get('HOST_NAME', ''), ]
    env.host_string = os.environ.get('HOST_NAME', '')

    env.base_image_name = os.environ.get('BASE_IMAGE_NAME', '')
    env.build_dir = '/srv/build'
    env.project_path = os.path.dirname(os.path.dirname((os.path.dirname(__file__))))

def compose(cmd='--help', path=''):
    """
    Wrapper for docker-compose
    """
    set_env()
    with cd(path):
        run('docker-compose {cmd}'.format(cmd=cmd))

def wheels():
    """
    Remotely build python binaries on image-factory server
    """
    set_env()
    with lcd(env.project_path):
        put('./requirements.txt', '/srv/build/wheel_requirements.txt')
        put('./etc/base_image/image_requirements.txt', '/srv/build/requirements.txt')

    with cd('/srv/build/wheelhouse'):
        run('rm -rf *.whl')

    compose(cmd='-f service.yml -p %s run --rm wheel-factory' % env.project_name, path='/srv/build')

def build():
    """
    Remotely build base python image with all installed packages on image-factory server
    """
    set_env()
    with lcd(env.project_path):
        put('./requirements.txt', '/srv/build/requirements.txt')

    with cd('/srv/build'):
        run('docker build -t {base_image_name} .'.format(
            base_image_name=env.base_image_name,
        ))

def docker(cmd='--help'):
    """
    Wrapper for docker
    """
    set_env()
    template = 'docker {cmd}'.format(cmd=cmd)
    run(template)

def push():
    """
    Push base docker image
    """
    set_env()
    docker('login')
    docker('push %s' % env.base_image_name)
