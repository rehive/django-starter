import os

# Check if debug variable is there to determine whether loaded
env_vars_loaded = os.environ.get('DEBUG', '')

# fallback for when env variables are not loaded:
if not env_vars_loaded:
    try:
        print('Loading keys from file...')
        current_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        parent_directory = os.path.split(current_directory)[0]
        parent_directory = os.path.split(parent_directory)[0]
        print(parent_directory)

        file_path = os.path.join(parent_directory, './.local.env')
        with open(file_path, 'r') as f:
            output = f.read()
            output = output.split('\n')

        for var in output:
            if var:
                k, v = var.split('=', maxsplit=1)
                os.environ.setdefault(k, v)
    except FileNotFoundError:
        print('environmental variables file not found')
        pass

# Add all project configurations that are stored in env variables:

# config
DEBUG = os.environ.get('DEBUG', '') in ['True', True, 'true']

# secrets
SECRET_KEY = os.environ.get('DJANGO_SECRET', '13&wd9&48$jv82^b#ygwu#fm+8l8orx2s5dh(90o3meuevngh!')

# AWS
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')