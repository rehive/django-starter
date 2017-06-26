from fabric.api import env, local, run, cd
import dotenv
import os

# Load local .env file
from fabric.contrib.project import rsync_project, upload_project
from fabric.operations import sudo

env.local_dotenv_path = os.path.join(
    os.path.dirname(__file__), './.server.env')
env.local_dir = os.path.dirname(__file__)
dotenv.load_dotenv(env.local_dotenv_path)

# Set Fabric env
env.use_ssh_config = True
env.hosts = [os.environ.get('HOST_NAME', ''), ]

env.digital_ocean_token = os.environ.get('DIGITAL_OCEAN_TOKEN', '')
env.host_name = os.environ.get('HOST_NAME', '')

env.username = os.environ.get('SSH_USERNAME', 'ubuntu')
env.sshd_port = os.environ.get('SSH_PORT', '22')
env.docker_compose_version = os.environ.get('DOCKER_COMPOSE_VERSION', '1.5.2')


# How to create default deployment
def provision(provider='digitalocean'):
    if provider == 'digitalocean':
        local('docker-machine create '
              '--driver digitalocean '
              '--digitalocean-region=ams2 '
              '--digitalocean-size=1gb '
              '--digitalocean-access-token={digital_ocean_token} '
              '--digitalocean-ssh-user {user}'
              '{host_name}'.format(digital_ocean_token=env.digital_ocean_token,
                                   user=env.username,
                                   host_name=env.host_name))

    # for gcloud, first install gcloud and do gcloud auth login
    elif provider == 'gcloud':
        local('docker-machine create '
              '--driver google '
              '--google-project play-server '
              '--google-zone europe-west1-c '
              '--google-machine-type g1-small '
              '--google-disk-size 20 '
              '--google-disk-type pd-standard '
              '--google-username {user} '
              '{host_name}'.format(host_name=env.host_name, user=env.username))


def ssh_config():
    ip_address = local(
        'docker-machine ip {host_name}'.format(host_name=env.host_name), capture=True)
    keyfile = '~/.docker/machine/machines/{host_name}/id_rsa'.format(
        host_name=env.host_name)

    ssh_config = env.ssh_config_template.format(
        host_name=env.host_name,
        ip=ip_address,
        port=env.sshd_port,
        user=env.username,
        keyfile=keyfile,
    )
    local('echo "\nHost {host_name}\n\tHostName {ip}\n\tPort {ssh_port}\n\tUser {user}\n\tIdentityFile {keyfile}"'
          '>> ~/.ssh/config'.format(host_name=env.host_name,
                                    ip=ip_address,
                                    ssh_port=env.sshd_port,
                                    user=env.username,
                                    keyfile=keyfile))
    print(ssh_config)


env.ssh_config_template = """Host {host_name}
    HostName {ip}
    Port {port}
    User {user}
    IdentityFile {keyfile}

"""


def install():
    # Add user to sudo:
    sudo('adduser {user} sudo'.format(user=env.username))

    # Install Docker Compose:
    sudo('curl -L '
         'https://github.com/docker/compose/releases/download/{docker_compose_version}/'
         'docker-compose-`uname -s`-`uname -m`'
         ' > /usr/local/bin/docker-compose'.format(docker_compose_version=env.docker_compose_version))

    sudo('chmod +x /usr/local/bin/docker-compose')

    # Add user to docker group:
    sudo('gpasswd -a {user} docker'.format(user=env.username))
    sudo('service docker restart')

    # Create server directory structure:
    sudo("mkdir -p /srv/certs /srv/config /srv/apps/default /srv/htdocs /srv/build")
    sudo("chown -R %s:%s /srv/" % (env.username, env.username))

def nginx_letsencrypt():
    upload_project(os.path.join(
        env.local_dir, 'docker-services.yml'), '/srv/', use_sudo=True)
    run('docker-compose -f /srv/docker-services.yml up -d nginx-proxy letsencrypt-plugin')
