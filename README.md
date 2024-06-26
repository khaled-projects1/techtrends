Project: TechTrends
Description: Apply Best Practices For Application Deployment

Steps:
  - Create a “/healthz” endpoint returning a 200 HTTP JSON response with a message “OK - healthy”.
  - Create a “/metrics” endpoint returning a 200 HTTP JSON response with “post_count” and “db_connection_count”.
  - Add logs to the application for various events, ensuring each logline has a timestamp.

Docker for Application Packaging:
  - Create a Dockerfile with:
    - Base image: Python 2.7
    - Expose port: 3111
    - Install packages from requirements.txt
    - Ensure database initialization with init_db.py
    - Run the application on container start
  - Build and push the Docker image:
    - Tag: “techtrends”
    - Specify the Dockerfile location
    - Save Docker commands in the "docker_commands" file
  - Test the Docker image locally:
    - Run in detached mode on port “7111”
    - Ensure application accessibility at “http://127.0.0.1:7111”
    - Save a screenshot of the output in "screenshots/docker-run-local"
    - Log the Docker commands and container logs in the "docker_commands" file

Continuous Integration with GitHub Actions:
  - Create a GitHub Action to build and push the application on every push to the main branch:
    - Use “ubuntu-latest” OS
    - Set context to the project directory
    - Reference TechTrends Dockerfile
    - Push image to DockerHub with tag “techtrends:latest”
  - Save screenshots of the successful build and DockerHub image in the "screenshots" folder with names “ci-github-actions” and “ci-dockerhub”

Kubernetes Declarative Manifest:
  - Deploy a Kubernetes cluster using k3s and Vagrant:
    - Save a screenshot of “kubectl get no” output in "screenshots/k8s-nodes"
  - Create Kubernetes declarative manifests:
    - Namespace: sandbox
    - Deployment: techtrends with image “techtrends:latest”, 1 replica, specific resource requests and limits, port 3111, and health checks
    - Service: techtrends with ClusterIP type, exposed port 4111, and target port 3111
  - Apply the manifests and save a screenshot of “kubectl get all -n sandbox” output in "screenshots/kubernetes-declarative-manifests"

Helm Charts:
  - Create a Helm Chart in the "helm" folder with:
    - Chart.yaml: apiVersion: v1, name: techtrends, version: 1.0.0
    - Templates for namespace, deployment, and service manifests
    - Default values: namespace sandbox, service port 4111, image “techtrends:latest” with pull policy “IfNotPresent”, 1 replica, specific resource requests and limits, port 3111, and health checks
  - Create custom values files for staging and production environments:
    - Values-staging.yaml: namespace staging, service port 5111, 3 replicas, specific resource requests and limits
    - Values-prod.yaml: namespace prod, service port 7111, image pull policy “Always”, 5 replicas, specific resource requests and limits

Continuous Delivery with ArgoCD:
  - Install ArgoCD and expose it through a NodePort service:
    - Save a screenshot of the ArgoCD UI in "screenshots/argocd-ui"
  - Build ArgoCD Application manifests using the TechTrends Helm chart:
    - For staging: helm-techtrends-staging.yaml with name techtrends-staging and reference values file values-staging.yaml
    - For prod: helm-techtrends-prod.yaml with name techtrends-prod and reference values file values-prod.yaml
  - Deploy TechTrends with ArgoCD:
    - Use kubectl to deploy the ArgoCD Application resources
    - Synchronize the applications and ensure namespaces, deployments, and services are up and running
    - Save screenshots of synchronized resources in "screenshots" with names “argocd-techtrends-staging” and “argocd-techtrends-prod”

