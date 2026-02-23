# DevOps Project: CI/CD + IaC + K8s + Monitoring

End-to-end DevOps project that builds and deploys a Flask app using:
- **Git/GitHub** for version control
- **Jenkins** for CI/CD
- **Docker** for containerization
- **Terraform** for infrastructure
- **Ansible** for server configuration (optional to run from EC2)
- **Kubernetes (kind)** for deployment
- **Prometheus & Grafana** for monitoring

> Designed to start beginner-friendly and scale to intermediate.

---

## 📁 Repository Structure
my-devops-project/
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── jenkins/
│   └── Jenkinsfile
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── ansible/
│   └── setup.yml        # (run from EC2 or any Linux machine; not required on Windows)
└── k8s/
├── namespace.yaml
├── deployment.yaml
├── service.yaml
└── kustomization.yaml

## 🧪 Application

- Simple **Flask** app exposing `/` and `/metrics` (Prometheus format)
- Dockerized with a **Python 3.11** slim image

---

## 🚀 CI/CD Flow (What Jenkins Will Do)

1. Checkout code from GitHub  
2. Build Docker image and tag `latest` + build number  
3. Push to Docker Hub  
4. Apply Kubernetes manifests and update image to current build  
5. Smoke-test by listing pods and service

> Configure Jenkins credentials:
> - `dockerhub-username` (Secret text)  
> - `dockerhub-password` (Secret text)

Update the Jenkinsfile:
```groovy
environment {
  DOCKERHUB_USER = 'YOUR_DOCKERHUB_USERNAME'
}


☁️ Infrastructure (Terraform)
Creates:

EC2 (Ubuntu 22.04)
Security Group (SSH 22, HTTP 80, Jenkins 8080, NodePorts 30000–30100)

Usage:

cd terraform
terraform init
terraform plan -var="key_name=<your-aws-keypair>"
terraform apply -var="key_name=<your-aws-keypair>" -auto-approve


Outputs include:

public_ip, public_dns, and an example ssh_command


🛠️ Server Setup (Ansible – optional to run from EC2)
Playbook installs:

Docker, Jenkins, kubectl, kind, Helm
Creates a kind cluster (devops)
Installs kube-prometheus-stack (Grafana NodePort 30030, Prometheus NodePort 30090)
Sets up kubeconfig for ubuntu and jenkins users

Run (from EC2 or any Linux with Ansible):

ansible-playbook -i "ec2 ansible_host=<EC2_PUBLIC_IP> ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/<key>.pem," \
  ansible/setup.yml
  
(Note the trailing comma in the inline inventory)

☸️ Kubernetes
Apply with:
kubectl apply -k k8s/

Service (NodePort 30080) exposes the app:

http://<EC2_PUBLIC_IP>:30080/


📊 Monitoring

Prometheus: http://<EC2_PUBLIC_IP>:30090/
Grafana:    http://<EC2_PUBLIC_IP>:30030/

Get Grafana admin password:

kubectl -n monitoring get secret kube-prometheus-stack-grafana \
  -o jsonpath="{.data.admin-password}" | base64 -d; echo
  
  
🔐 Security & Next Steps

Use Jenkins credentials for secrets
Add automated tests (pytest) and linters (flake8)
Replace kind with managed K8s (EKS/AKS/GKE) later
Use Ingress + TLS (cert-manager) instead of NodePorts for production

# (on EC2) remove kind cluster
kind delete cluster --name devops || true

# (locally) destroy infra
cd terraform
terraform destroy -var="key_name=<your-aws-keypair>" -auto-approve
