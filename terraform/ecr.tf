# ============================================================
# ECR ARCHITECTURE
#
# Developer
#     ↓
# Docker Build
#     ↓
# Amazon ECR
#     ↓
# EKS pulls image
#     ↓
# Kubernetes Pod
#
# ============================================================


# ============================================================
# ECR REPOSITORY
# ============================================================

resource "aws_ecr_repository" "logistics" {
  name                 = "${var.environment}/${var.project_name}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name        = "${var.project_name}-ecr"
    Environment = var.environment
  }
}