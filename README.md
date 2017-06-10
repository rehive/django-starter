Django starter project
======================
Local development
-----------------
1. Set up a python virtual environment. E.g. with Anaconda:
`conda create -n django-starter python=3`  
`source activate django-starter`  
`pip install -r requirements.txt`

If psycopg2 installation fails to install, try `conda install psycopg2==2.6.2`

2. Install `invoke` and related libraries in your virtual environment (you can do this in a separate environment if you prefer):  
`pip install invoke`  
`pip install python-dotenv`  
`pip install fabric3`  
`pip install pyyaml`  
`pip install semver`  

3. Add the project name and details to as well as the virtual environment path to local.yaml and use `.local.env.example` as a template to create a `.local.env` with the project environmental variables.

3. Start the postgres database:  
`inv local.compose -c 'up -d postgres'`

4. Start the webserver on port 8000:  
`inv local.manage runserver`

Automated Deployment:
-----------------
TODO

Manual deployment:
------------------
### Push to container registry:
1. Build the static webserver:  
   `inv k8s.build -c production -v v0.001`  
4. Deploy to Kubernetes Cluster:  
    `inv deploy -c production.yaml -v v0.001` . 

### Once-off build-server setup:
1.
2. Provision the virtual machine:  
`fab -f ./etc/base_image/server/fabric_tasks.py create:provider='digitalocean'`  
3. Add the machine to your SSH config
`fab -f ./etc/base_image/server/fabric_tasks.py add`  
`fab -f ./etc/base_image/server/fabric_tasks.py install`
`fab -f ./etc/base_image/server/fabric_tasks.py factory`   

### Once-off Kubernetes Cluster Setup:
1. Create a Kubernetes Cluster
2. Athenticate gcloud:    
    `gcloud auth login`  
    `gcloud config set project {project-name}`  
3. Connect to kubernetes cluster:  
    `gcloud container clusters get-credentials {cluster-name} --zone us-west1-a --project {project-name}`  
4. Letsencrypt SSL setup:  
    `kubectl apply -f etc/k8s/lego/00-namespace.yaml && kubectl apply -f etc/k8s/lego/configmap.yaml && kubectl apply -f etc/k8s/lego/deployment.yaml`  
5. Webserver setup:  
    `inv templater production` (templater is not yet very smart. you will need to manually configure things like multiple domains)
	`inv setup production`  
6. Check the external IP address and setup DNS:  
    `inv ip production`  
