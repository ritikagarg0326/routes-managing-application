# LogiOps - AWS DevOps Demo Project

A Python Flask logistics routes  management application designed to demonstrate an end-to-end DevOps workflow.

## Features

- Dashboard
- Truck management
- Route management and route selection
- Supplier and supplier-manager management
- Product inventory
- Jira/operations ticket tracking
- Health endpoint: `/api/health`
- Metrics endpoint: `/api/stats`

## Local setup

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

The local default database is SQLite. For AWS Aurora PostgreSQL, set:

```bash
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME
```

## Docker

```bash
docker build -t logistics-app .
docker run -p 5000:5000 logistics-app
```

## AWS architecture used for interview/demo

Developer
  -> GitHub
  -> GitHub Actions
  -> Docker build
  -> Amazon ECR
  -> ECS task definition
  -> ECS service
  -> Application

Supporting services:
- Aurora PostgreSQL: relational data
- API Gateway/Lambda: optional serverless APIs
- S3: static/object storage
- CloudWatch: metrics/logs/alarms
- Slack: alert notifications
- Jira: work/ticket tracking

## GitHub Actions

The workflow in `.github/workflows/ci-cd.yml`:
1. Checks out source.
2. Authenticates to AWS.
3. Logs in to ECR.
4. Builds a Docker image tagged with the Git commit SHA.
5. Pushes the image to ECR.
6. Renders the ECS task definition with the new image.
7. Deploys the new task definition to ECS.
8. Waits for ECS service stability.

For production, prefer GitHub OIDC with an IAM role instead of long-lived AWS access keys.

## Important production improvements

This demo intentionally keeps the application simple. For a real production deployment:
- Store secrets in AWS Secrets Manager or SSM Parameter Store.
- Use Aurora PostgreSQL instead of SQLite.
- Use private subnets for ECS/Aurora where appropriate.
- Put ECS behind an Application Load Balancer.
- Add HTTPS using ACM.
- Add authentication/authorization.
- Add database migrations.
- Add tests and security scanning.
- Use GitHub OIDC instead of static AWS credentials.
- Add CloudWatch alarms for CPU, memory, 5xx, target health, task count, latency and Aurora health.
- Send alarms to SNS and integrate SNS with Slack or an approved incident-management integration.
- Use separate Dev/Pre-Stage/Prod AWS resources and controlled promotion.

## Jira

Jira remains the work-management system. A typical ticket lifecycle is:

Jira ticket -> developer change -> GitHub PR -> GitHub Actions -> ECR -> ECS -> validation -> Jira update.

This demo provides local ticket tracking so the workflow can be demonstrated without requiring a Jira account. A production version can integrate the Jira REST API.


eks cluster validated
GITHUB ACTION WORKFLOW AUOTMATED TO BUILD TEST AND DEPLOY IN EKS CLUSTER
