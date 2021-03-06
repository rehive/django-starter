from invoke import task
import json
import yaml
import semver
import dotenv

from fabric.api import run, local
from fabric.tasks import execute

import fabfile as fab

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


# Build Server Commands:
@task
def upload(ctx, config):
    """Rsync project to server"""
    execute(fab.set_env, config)
    execute(fab.upload)

@task
def build(ctx, config, version_tag, packages=False):
    """
    Build project's docker image on remote server using fabric
    """
    upload(ctx, config)
    execute(fab.set_env, config, version_tag)
    execute(fab.build)

@task
def push(ctx, config, version_tag):
    """Push image to container registry"""
    execute(fab.set_env, config, version_tag)
    execute(fab.push)

@task
def compose(ctx, cmd, config, version_tag):
    """Push image to container registry"""
    execute(fab.set_env, config, version_tag)
    execute(fab.compose, cmd, version_tag)
