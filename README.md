Django starter project
======================
Local development
-----------------
1. Set up a python virtual environment. E.g. with Anaconda:
`conda create -n django-starter python=3.5`  
`source activate django-starter`  
`pip install -r requirements.txt`

If psycopg2 installation fails to install, try `conda install psycopg2==2.6.2`

2. Install `invoke` and related libraries in your virtual environment (you can do this in a separate environment if you prefer):  
`pip install invoke python-dotenv fabric3 pyyaml semver`  

3. Add the project name and details to as well as the virtual environment path to `local.yaml.` For Anaconda, if you don't know the path to your virtual environment, you can run `which python` from within your virtual environment to find your virtual environment path.

4. Use `.local.env.example` as a template to create a `.local.env` with the project environmental variables.  
 One-liner for django secret key generation:
 `python -c "import string,random; uni=string.ascii_letters+string.digits+string.punctuation; print repr(''.join([random.SystemRandom().choice(uni) for i in range(random.randint(45,50))]))"`

6. Start the postgres database:  
`inv local.compose -c 'up -d postgres'`

7. Check if Docker is running:
`docker ps` or `inv local.compose -c ps`

8. Migrate database:
`inv local.manage migrate`

9. Start the webserver on port 8000:  
`inv local.manage 'runserver --insecure'`