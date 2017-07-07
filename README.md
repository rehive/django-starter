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

Provisioning virtual machine on cloud provider (Optional)
---------------------------------------------------------

1. `cd etc/server`

2. Create your own `.server.env` by copying `.server.env.example`

3. Set your 'HOST NAME' to describe your server. For Google Cloud use `USERNAME:ubuntu`  for Digital Ocean use `USERNAME:root`. Furthermore, for Digital Ocean add your token, whereas for Google Cloud you have to install Google Cloud SDK.

4. Make sure `fabric3` is installed in your Python virtual environment. Activate your Python virtual environment, e.g. `source activate django-starter`.

5. Edit the provision function in fabfile.py:
- For Google Cloud set your project name and machine settings. 
- For Digital Ocean set your machine settings.

6. Run `fab provision:gcloud`

7. Run `fab ssh_config`

8. Run `fab install`

9. Run `fab nginx_letsencrypt`


Deploy to virtual machine on cloud provider (Optional)
------------------------------------------------------

1. Provision your cloud server. Follow the steps above or look at the code in fabfile.py if you want to do it yourself.  

2. Create .production.yaml and .production.env using .production.yaml.example and production.env.example as reference. The HOST_NAME variable should be the same as that set up for your provisioned machine in ~/.ssh/config, as was done in the steps above.  

3. Set the VIRTUAL_HOST and LETSENCRYPT_HOST parameters to your domain name and then go to your domain's DNS settings and create an A record pointing to the IP address of your virtual machine. The nginx-proxy and letsencrypt-plugin docker containers should then take care of the rest when you deploy and automatically generate and configure SSL certificates.  

4. Build your docker image on the server (the last parameter is the version numnber):  
   `inv server.build staging 0.0.1`  
   `inv server.push staging 0.0.1`  
   
5. Run your server:  
    `inv compose up staging 0.0.1`  
