from invoke import task
import json
import yaml
import semver
import dotenv
import os


def get_config(config):
    """Import config file as dictionary"""
    if config[-5:] != '.yaml':
        config += '.yaml'

    dir_path = os.path.dirname(os.path.realpath(__file__))
    server_dir_path = dir_path
    if not os.path.isabs(config):
        config = os.path.join(server_dir_path, config)

    with open(config, 'r') as stream:
        config_dict = yaml.load(stream)

    return config_dict


@task
def compose(ctx, cmd='--help', version='latest'):
    """
    Local only function: Wrapper for docker-compose
    """
    config_dict = get_config('local')
    image_name = config_dict['IMAGE']
    if version:
        image_name += ':' + version

    dir_path = os.path.dirname(os.path.realpath(__file__))
    env_file = os.path.join(dir_path, config_dict.get('ENV_FILE', ''))

    env_vars = ("IMAGE_NAME={image_name} "
                "ENV_FILE={env_file} "
                "CELERY_ID={celery_id}  "
                "COMPOSE_PROJECT_NAME={compose_project_name} "
                "POSTGRES_PORT={postgres_port} "
                ).format(image_name=image_name,
                         env_file=env_file,
                         celery_id=config_dict.get('CELERY_ID', ''),
                         compose_project_name=config_dict['PROJECT_NAME'],
                         postgres_port=config_dict.get('POSTGRES_PORT', 5432))

    path = 'etc/compose/docker-compose.yml'

    ctx.run(
        '{env} docker-compose -f {path} {cmd}'.format(env=env_vars, cmd=cmd, path=path))


@task
def manage(ctx, cmd):
    """Wrapper for manage function"""
    config_dict = get_config('local')
    venv_python = config_dict['VENV_PYTHON']

    # Switched to run via fabric as invoke was not displaying stdout correctly
    ctx.run('{python} src/manage.py {cmd}'.format(python=venv_python, cmd=cmd), pty=True)

@task
def build(ctx, config, version_tag):
    """
    Build project's docker image
    """
    config_dict = get_config(config)
    image_name = config_dict['IMAGE'].split(':')[0]
    image = '{}:{}'.format(image_name, version_tag)

    cmd = 'docker build -t %s .' % image
    ctx.run(cmd, echo=True)
    return image


@task
def push(ctx, config, version_tag):
    """
    Build, tag and push docker image
    """
    config_dict = get_config(config)
    image_name = config_dict['IMAGE'].split(':')[0]
    image = '{}:{}'.format(image_name, version_tag)

    ctx.run('gcloud docker -- push %s' % image, echo=True)