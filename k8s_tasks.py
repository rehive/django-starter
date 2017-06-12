from invoke import task
import fabfile as fab
import json
import yaml
import semver
import dotenv

import os

# Utility functions

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


def get_workers(config):
    """Import workers config file as dictionary"""
    if config[-5:] != '.json':
        config += '.json'

    # Use /server as base path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    server_dir_path = dir_path
    if not os.path.isabs(config):
        config = os.path.join(server_dir_path, config)

    with open(config, 'r') as stream:
        workers_dict = json.load(stream)

    return workers_dict


@task
def templater(ctx, config, template='etc/k8s/templates/all-in-one.yaml'):
    """ Creates deployment setup for given config file"""

    config_dict = get_config(config)

    # Get path of tasks.py file to allow independence from CWD
    dir_path = os.path.dirname(os.path.realpath(__file__))

    if not os.path.isabs(template):
        template = os.path.join(dir_path, template)
    with open(template, 'r') as myfile:
        template_str = myfile.read()

    formatted = format_yaml(template_str, config_dict)
    output_dir = os.path.join(dir_path, 'etc/k8s', config_dict['NAMESPACE'])
    output_path = os.path.join(output_dir, 'all-in-one.yaml')
    if os.path.isfile(output_path):
        print('Deployment config already exists. Aborting.')
    else:
        os.mkdir(output_dir)
        with open(output_path, 'w') as myfile:
            myfile.write(formatted)


@task
def deploy(ctx, config, version_tag):
    """
    Updates kubernetes deployment to use specified version
    """

    config_dict = get_config(config)
    workers_dict = get_workers('etc/k8s/bitcoin-hooks-staging/workers.json')

    image_name = config_dict['IMAGE'].split(':')[0]
    image = '{}:{}'.format(image_name, version_tag)

    ctx.run('kubectl set image deployment/{} '
            '{}={} --namespace={}'.format('webapp',
                                          config_dict['PROJECT_NAME'],
                                          image,
                                          config_dict['NAMESPACE']), echo=True)

    for worker in workers_dict.keys():
        ctx.run('kubectl set image deployment/{} '
                '{}={} --namespace={}'.format(worker,
                                              config_dict['PROJECT_NAME'],
                                              image,
                                              config_dict['NAMESPACE']), echo=True)


@task
def setup_workers(ctx, config):
    """
    Updates kubernetes deployment to use specified version
    """

    config_dict = get_config(config)
    workers_dict = get_workers('etc/k8s/bitcoin-hooks-staging/workers.json')

    ctx.run(
        'kubectl apply -f etc/k8s/{}/workers.yaml'.format(config_dict['NAMESPACE']))

    for worker, queue in workers_dict.items():
        ctx.run('kubectl set command deployment/{worker} '
                '[\'bash\',\'-c\',\'celery -A config.celery worker '
                '--loglevel=INFO --concurrency=1 -Q {queue}-{celery_id} '
                '--namespace={namespace}\']'.format(worker=worker,
                                                    queue=queue,
                                                    celery_id=config_dict['CELERY_ID'],
                                                    namespace=config_dict['NAMESPACE']), echo=True)

# Wrapper Functions:


@task
def kubectl(ctx, config, cmd):
    """Wrapper for the kubectl command"""
    config_dict = get_config(config)
    ctx.run('kubectl {cmd} --namespace {namespace}'.format(cmd=cmd,
                                                           namespace=config_dict['NAMESPACE']))


@task
def run(ctx, config, version_tag, cmd, env=""):
    """Wrapper for kubectl run"""
    config_dict = get_config(config)

    image_name = config_dict['IMAGE'].split(':')[0]
    image = '{}:{}'.format(image_name, version_tag)

    kubectl(ctx,
            config,
            'run --image={image} '
            '{project_name}-run {cmd} '
            '--restart="Never" '
            '--env {env} '
            '--attach=True --rm=True'.format(image=image,
                                             project_name=config_dict['PROJECT_NAME'],
                                             cmd=cmd,
                                             env=env))


@task
def manage(ctx, config, version_tag, cmd):
    """Wrappper for django's manage.py"""
    env = '\"DEBUG=FALSE,POSTGRES_DB={postgres_db},POSTGRES_USER={postgres_user},POSTGRES_PASSWORD={postgres_password}\"'.format(postgres_db='monkey_db',
                                                                                                                                 postgres_user='monkey_user',
                                                                                                                                 postgres_password='monkey_pass')
    run(ctx, config, version_tag,
        'python manage.py {cmd}'.format(cmd=cmd), env)


@task
def get_env(ctx, config):
    """Read env variables from file"""
    if config[-5:] == '.yaml':
        config = config[:-5]
    file_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), '.' + config + '.env')
    with open(file_path, 'r') as f:
        output = f.read()
        output = output.split('\n')
    env_dict = {k: v for k, v in (line.split(
        '=', maxsplit=1) for line in output)}
    return env_dict


@task
def upload_static(ctx, config):
    """Upload static files to gcloud bucket"""
    env_dict = get_env(ctx, config)
    venv_python = env_dict['VENV_PYTHON']

    ctx.run(
        'echo "yes\n" | {python} src/manage.py collectstatic'.format(python=venv_python))
    ctx.run('gsutil -m rsync -d -r var/www/static gs://' +
            env_dict['GCLOUD_STATIC_BUCKET'] + '/')


@task
def create_bucket(ctx, config):
    """Creates gcloud bucket for static files"""
    env_dict = get_env(ctx, config)
    bucket_name = env_dict['GCLOUD_STATIC_BUCKET']
    ctx.run('gsutil mb gs://{bucket_name}'.format(bucket_name=bucket_name))
    ctx.run(
        'gsutil defacl set public-read gs://{bucket_name}'.format(bucket_name=bucket_name))


@task
def setup(ctx, config):
    """
    Updates kubernetes deployment to use specified version
    """
    config_dict = get_config(config)
    ctx.run(
        'kubectl apply -f etc/k8s/{}/all-in-one.yaml'.format(config_dict['NAMESPACE']))


@task
def secret(ctx, config):
    """
    Updates kubernetes deployment to use specified version
    """
    config_dict = get_config(config)
    ctx.run(
        'kubectl apply -f etc/k8s/{}/.secret.yaml'.format(config_dict['NAMESPACE']))


@task
def pgpool(ctx, config):
    """
    Updates kubernetes deployment to use specified version
    """
    config_dict = get_config(config)
    ctx.run(
        'kubectl apply -f etc/k8s/{}/database-service/pgpool.yaml'.format(config_dict['NAMESPACE']))


@task
def configmap(ctx, config):
    """
    Updates kubernetes deployment to use specified version
    """
    config_dict = get_config(config)
    ctx.run(
        'kubectl apply -f etc/k8s/{}/configmap.yaml'.format(config_dict['NAMESPACE']))


@task
def ip(ctx, config):
    """
    Updates kubernetes deployment to use specified version
    """

    config_dict = get_config(config)
    ctx.run('kubectl get ingress --namespace {} {}'.format(config_dict['NAMESPACE'],
                                                           config_dict['PROJECT_NAME']), echo=True)


@task
def live(ctx, config):
    """Checks which version_tag is live"""
    config_dict = get_config(config)

    result = ctx.run('kubectl get deployment/{} --output=json --namespace={}'.format('webapp',
                                                                                     config_dict['NAMESPACE']),
                     echo=True,
                     hide='stdout')

    server_config = json.loads(result.stdout)
    image = server_config['spec']['template']['spec']['containers'][0]['image']
    print(image)
    return image
