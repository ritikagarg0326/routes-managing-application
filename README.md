# LogiOps — Kubernetes-Native Logistics DevOps Platform

A hands-on **Python Flask logistics application** deployed on **Amazon EKS** with Docker, Amazon ECR, Helm, GitHub Actions CI/CD, AWS Load Balancing, IAM/EKS access controls, PostgreSQL, and Prometheus/Grafana observability.

The project demonstrates the complete DevOps flow from **source code → container image → registry → Kubernetes deployment → public application → monitoring**.

## 🚀 Application

LogiOps provides:

- Dashboard
- Truck management
- Route management
- Supplier management
- Product inventory
- Jira/operations ticket tracking
- Health endpoint: `/api/health`
- Application metrics endpoint: `/api/stats`

## 🏗️ Architecture

```text
Developer
   |
   | git push
   v
GitHub Repository
   |
   v
GitHub Actions
   |
   +-------------------------+
   |                         |
   v                         v
CI: Build & Push       CD: Deploy to EKS
   |                         |
Docker Build            AWS Authentication
   |                         |
ECR Push                EKS Authentication
   |                         |
   |                    Helm Upgrade/Install
   |                         |
   +------------+------------+
                |
                v
        Amazon EKS Cluster
                |
       +--------+---------+
       |                  |
       v                  v
  LogiOps Pod       PostgreSQL Pod
       |                  |
       v                  v
Kubernetes Service   ClusterIP Service
       |
       v
AWS Load Balancer
       |
       v
     Users

Observability:
EKS → Prometheus → Grafana
```

## 🔄 CI/CD

Every push to `main` triggers GitHub Actions.

```text
git push
   ↓
Checkout
   ↓
AWS authentication
   ↓
Docker build
   ↓
SHA-tagged image
   ↓
Amazon ECR
   ↓
Update EKS kubeconfig
   ↓
Helm upgrade --install
   ↓
Kubernetes rollout
   ↓
Verify pods / services / deployments
```

### CI

The CI workflow:

1. Checks out source.
2. Authenticates to AWS.
3. Logs into Amazon ECR.
4. Builds the Docker image.
5. Tags the image with the Git commit SHA.
6. Pushes the image to ECR.

Example:

```text
470024785854.dkr.ecr.us-east-1.amazonaws.com/dev/logistics:<git-sha>
```

Using the commit SHA gives traceability between a Git commit and the image deployed to EKS.

### CD

The CD workflow:

1. Authenticates to AWS.
2. Updates kubeconfig for EKS.
3. Deploys the Helm release.
4. Overrides the image repository/tag.
5. Waits for rollout completion.
6. Verifies pods, services, deployments and ingress.

The pipeline was tested through multiple deployment iterations, including fixing image-tag propagation, Helm values, Kubernetes image errors and AWS Load Balancer configuration.

## ✅ GitHub Actions Evidence

![GitHub Actions CI/CD success](docs/images/github-actions-workflow-success.png)

![GitHub Actions workflow runs](docs/images/github-actions-runs.png)

![CD deployment verification](docs/images/github-actions-cd-verify.png)

## 🐳 Docker + Amazon ECR

```text
Flask Source
    ↓
Dockerfile
    ↓
Docker Image
    ↓
Amazon ECR
    ↓
Amazon EKS
```

Images are versioned with the Git SHA rather than relying only on `latest`.

Benefits:

- Immutable deployment versions
- Traceability
- Easier rollback
- Safer automated deployments

## ☸️ Amazon EKS

The application is deployed to an EKS cluster using Kubernetes and Helm.

```text
EKS
│
├── LogiOps Deployment
│   └── Flask Pod
│
├── PostgreSQL Deployment
│   └── PostgreSQL Pod
│
├── Services
│   ├── logistics
│   └── logistics-postgres
│
└── Ingress / Load Balancing
```

The deployment pipeline verifies the resulting Kubernetes state with commands equivalent to:

```bash
kubectl get pods
kubectl get svc
kubectl get deployments
kubectl get ingress
```

![EKS pods and services](docs/images/eks-pods-and-services.png)

## ⛵ Helm

The Kubernetes application is packaged as a Helm chart:

```text
helm/
└── logistics/
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
        ├── deployment.yaml
        ├── service.yaml
        ├── ingress.yaml
        ├── postgres-deployment.yaml
        └── postgres-service.yaml
```

Deployment:

```bash
helm upgrade --install logistics ./helm/logistics
```

The CD workflow passes the exact ECR image repository and Git SHA as Helm values.

This provides:

- Repeatable deployments
- Versioned Kubernetes configuration
- Environment-specific values
- Easier rollback
- Separation of application and deployment configuration

## 🌐 AWS Load Balancing

The application was exposed externally through a Kubernetes `LoadBalancer` Service backed by AWS.

```text
Internet
   ↓
AWS Load Balancer
   ↓
Kubernetes Service
   ↓
LogiOps Pod
```

![Application running through AWS Load Balancer](docs/images/application-running-on-aws-loadbalancer.png)

For the final service design, PostgreSQL is kept internal using `ClusterIP` rather than exposing the database publicly.

A more production-oriented evolution is:

```text
Route 53
   ↓
AWS Load Balancer Controller
   ↓
ALB / HTTPS
   ↓
Ingress
   ↓
ClusterIP Service
   ↓
Pods
```

## 🔐 AWS IAM and EKS Access

AWS IAM is used for AWS and EKS authentication.

The EKS cluster uses EKS access entries to grant the required IAM principals Kubernetes access.

The CI/CD workflow uses GitHub repository secrets for AWS authentication during this learning implementation.

For production, the preferred architecture is:

```text
GitHub Actions
      ↓
GitHub OIDC
      ↓
AWS IAM Role
      ↓
Short-lived credentials
      ↓
ECR / EKS
```

instead of long-lived AWS access keys.

## 📊 Prometheus + Grafana

The project includes Kubernetes observability using Prometheus and Grafana.

Prometheus collects metrics and Grafana visualizes them.

Metrics explored include:

- Pod CPU
- Pod memory
- Receive bandwidth
- Transmit bandwidth
- Packet rates
- Kubernetes workload metrics
- Pod-level resource usage

![Grafana CPU metrics](docs/images/grafana-kubernetes-cpu-metrics.png)

![Grafana network metrics](docs/images/grafana-kubernetes-network-metrics.png)

### Observability flow

```text
Kubernetes
    ↓
Metrics
    ↓
Prometheus
    ↓
Grafana
    ↓
Dashboards
```

This allows Kubernetes health and resource usage to be investigated without relying only on the AWS console.

## 🧪 Troubleshooting and Real Deployment Work

The project was developed through real deployment iterations and troubleshooting.

Issues handled included:

- Docker image/tag propagation
- ECR image deployment
- Kubernetes `ImagePullBackOff`
- Invalid image names
- Helm values/template errors
- Kubernetes Service configuration
- AWS Load Balancer exposure
- EKS IAM/access configuration
- Rolling pod replacement
- Deployment verification
- Separating public application access from internal PostgreSQL access

The CI/CD pipeline was ultimately configured so that the deployed EKS image corresponds to the exact Git commit SHA.

## 🛠️ Technology Stack

| Area | Technology |
|---|---|
| Application | Python Flask |
| Containerization | Docker |
| Source Control | Git / GitHub |
| CI/CD | GitHub Actions |
| Registry | Amazon ECR |
| Kubernetes | Amazon EKS |
| Packaging | Helm |
| Cloud | AWS |
| Infrastructure | Terraform |
| Database | PostgreSQL |
| Metrics | Prometheus |
| Dashboards | Grafana |
| Load Balancing | AWS Load Balancer |
| Access | AWS IAM / EKS Access Entries |

## 📁 Repository Structure

```text
routes-managing-application/
│
├── .github/
│   └── workflows/
│       ├── pipeline.yml
│       ├── reusable-ci.yml
│       └── reusable-cd.yml
│
├── backend/
├── frontend/
├── database/
│
├── helm/
│   └── logistics/
│
├── k8s/
├── terraform/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── app.py
└── README.md
```

## 🔑 GitHub Secrets

The learning implementation uses repository secrets such as:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

No AWS credentials are committed to the repository.

For production, GitHub OIDC with an AWS IAM role should replace long-lived credentials.

## 🎯 DevOps Skills Demonstrated

- Git and GitHub
- GitHub Actions
- Reusable CI/CD workflows
- Docker
- Amazon ECR
- Amazon EKS
- Kubernetes
- Helm
- Kubernetes Services
- AWS Load Balancing
- AWS IAM
- EKS Access Entries
- Terraform
- Prometheus
- Grafana
- PostgreSQL
- CI/CD automation
- Immutable image versioning
- Kubernetes rollout verification
- Kubernetes troubleshooting
- Helm troubleshooting
- Cloud infrastructure troubleshooting

## 🚀 Next Improvements

Planned production-oriented enhancements:

- GitHub OIDC
- AWS Load Balancer Controller + ALB
- Route 53 + custom domain
- ACM HTTPS
- Horizontal Pod Autoscaler
- Readiness/liveness probes
- Alertmanager
- Fluent Bit + centralized logging
- OpenSearch/Kibana
- AWS Secrets Manager / External Secrets
- Argo CD / GitOps
- AI-powered Kubernetes observability agent
- Automated CPU/memory alert investigation

## 💼 Resume / Interview Summary

> Built and deployed a containerized Python Flask logistics platform on Amazon EKS using Docker, Amazon ECR, Helm and GitHub Actions. Implemented reusable CI/CD workflows to build and push SHA-tagged images to ECR, automatically deploy Helm releases to EKS, and verify Kubernetes workloads after deployment. Configured AWS Load Balancing for external application access, IAM/EKS access controls, PostgreSQL services, and Prometheus/Grafana monitoring for Kubernetes resource and network metrics. Troubleshot Kubernetes image, Helm, IAM, service and deployment issues throughout the implementation.

## 📸 Project Evidence

Deployment screenshots are stored under:

```text
docs/images/
```

and referenced directly by this README so the repository serves as both the project documentation and visual proof of the implementation.
