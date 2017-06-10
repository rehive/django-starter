Bitcoin Monitoring
=============
Automated Deployment:
-----------------
TODO

Manual Deployment:
------------------
### Push to container registry:
1. Build the static webserver:  
   `inv build -c production -v v0.001`
2. Push to Container Registry:  
   `inv build -c production -v v0.001`
3. Run locally:  
    `inv run -c production -v v0.001`  
4. Deploy to Kubernetes Cluster:  
    `inv deploy -c production.yaml -v v0.001`

### Once-off build-server setup:
`fab -f ./etc/base_image/server/fabric_tasks.py create:provider='digitalocean'`
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