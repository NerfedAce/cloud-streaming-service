# ☁️ Cloud Streaming Service

A cloud-native video streaming application built with **React**, **FastAPI**, **PostgreSQL**, **AWS**, **Docker**, **Terraform**, and **Jenkins**.

This project demonstrates deploying and managing a full-stack application using modern DevOps practices. Users can upload videos, which are stored in **Amazon S3**, while application data is stored in **Amazon RDS PostgreSQL**. The frontend and backend are containerized using Docker and deployed on an **Amazon EC2** instance.

---

# Features

- User registration and login
- Upload videos to Amazon S3
- Stream videos directly from S3
- Store user information in PostgreSQL (Amazon RDS)
- View uploaded videos
- Dockerized frontend and backend
- Deploy entire application using Docker Compose
- Infrastructure provisioning using Terraform
- Automated deployment using Jenkins CI/CD
- Environment-based configuration

---

# Tech Stack

## Frontend

- React
- Vite
- Axios

## Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Boto3

## Infrastructure

- AWS EC2
- AWS RDS (PostgreSQL)
- AWS S3
- Docker
- Docker Compose
- Terraform
- Jenkins

---

# Architecture

```
                    GitHub
                       │
                 Jenkins Pipeline
                       │
            Build Docker Images
                       │
              Deploy to EC2
                       │
        ┌──────────────┴──────────────┐
        │                             │
   React Frontend               FastAPI Backend
                                       │
                      ┌────────────────┴──────────────┐
                      │                               │
               Amazon RDS PostgreSQL           Amazon S3 Bucket
```

---

# Prerequisites

Before deployment, ensure you have:

- AWS Account
- EC2 Key Pair
- Git
- Docker
- Docker Compose
- Terraform (optional if provisioning manually)

---

# AWS Setup

## 1. Create an Amazon S3 Bucket

1. Open AWS Console.
2. Navigate to **S3**.
3. Create a new bucket.
4. Choose a globally unique bucket name.
5. Select your preferred AWS region.
6. Keep Block Public Access enabled (recommended).
7. Create the bucket.

Example:

```
cloud-streaming-service
```

---

## 2. Create an IAM User

Create an IAM user with programmatic access.

Grant the following permissions:

- AmazonS3FullAccess

Save the following credentials:

- Access Key ID
- Secret Access Key

These credentials will be used by the backend to upload and retrieve videos.

---

## 3. Create an Amazon RDS PostgreSQL Database

Navigate to:

AWS Console → RDS → Create Database

Recommended configuration:

- Engine: PostgreSQL
- Template: Free Tier
- Instance: db.t3.micro
- Storage: 20 GB
- Public Access: Yes (Development)
- Create a database username and password.

After creation, note the following:

- Database Endpoint
- Port
- Database Name
- Username
- Password

Example:

```
Endpoint:
mydatabase.xxxxxxxxx.ap-south-1.rds.amazonaws.com

Port:
5432
```

---

## 4. Configure the RDS Security Group

Allow inbound PostgreSQL traffic on port **5432** from your EC2 instance's security group.

Without this rule, the backend will not be able to connect to the database.

---

## 5. Launch an EC2 Instance

Recommended configuration:

- Ubuntu Server 24.04 LTS
- t2.micro or t3.micro
- Root Volume: **20 GB**

Configure the Security Group to allow:

| Port | Purpose |
|------|----------|
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS (optional) |
| 8000 | FastAPI |
| 3000 | React (optional during development) |

Connect using SSH:

```bash
ssh -i your-key.pem ubuntu@YOUR_PUBLIC_IP
```

---

# Install Docker

Update packages:

```bash
sudo apt update
```

Install Docker:

```bash
sudo apt install docker.io docker-compose-v2 -y
```

Allow the current user to run Docker:

```bash
sudo usermod -aG docker ubuntu

newgrp docker
```

Verify installation:

```bash
docker --version

docker compose version
```

---

# Clone the Repository

```bash
git clone https://github.com/NerfedAce/cloud-streaming-service.git

cd cloud-streaming-service
```

---

# Environment Configuration

## Root `.env`

Create a file named:

```
.env
```

Example:

```env
DB_HOST=YOUR_RDS_ENDPOINT
DB_PORT=5432
DB_NAME=cloudstream
DB_USER=postgres
DB_PASSWORD=password

AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
AWS_REGION=ap-south-1

S3_BUCKET=cloud-streaming-service
```

---

## Frontend Environment

Create:

```
frontend/.env
```

Example:

```env
VITE_API_URL=http://YOUR_EC2_PUBLIC_IP:8000
```

Example:

```env
VITE_API_URL=http://13.233.xxx.xxx:8000
```

---

# Connecting to Amazon RDS

The backend automatically connects using the following environment variables:

```env
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

Ensure:

- The RDS instance is running.
- The endpoint is correct.
- The EC2 security group has permission to access port **5432**.

---

# Connecting to Amazon S3

The backend uses **boto3** for interacting with Amazon S3.

Required environment variables:

```env
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
S3_BUCKET
```

Uploaded videos are stored in the configured S3 bucket and streamed from there.

---

# Running the Application

Build and start all services:

```bash
docker compose up --build -d
```

View logs:

```bash
docker compose logs -f
```

Stop the application:

```bash
docker compose down
```

---

# Access the Application

Frontend:

```
http://YOUR_EC2_PUBLIC_IP
```

Backend:

```
http://YOUR_EC2_PUBLIC_IP:8000
```

FastAPI Documentation:

```
http://YOUR_EC2_PUBLIC_IP:8000/docs
```

---

# Updating the Application

Pull the latest changes:

```bash
git pull
```

Rebuild containers:

```bash
docker compose down

docker compose up --build -d
```

---

# Troubleshooting

## Unable to connect to PostgreSQL

- Verify the RDS instance is running.
- Check the database credentials.
- Confirm the endpoint is correct.
- Ensure port **5432** is open from the EC2 security group.

---

## Unable to upload videos

Check:

- IAM credentials
- Bucket name
- AWS Region
- S3 permissions

---

## Frontend cannot communicate with the backend

Verify:

```
frontend/.env
```

contains the correct backend URL:

```env
VITE_API_URL=http://YOUR_EC2_PUBLIC_IP:8000
```

Then rebuild the frontend.

---

## Docker containers fail to start

Inspect the logs:

```bash
docker compose logs
```

---

# Project Structure

```
cloud-streaming-service/
│
├── backend/
├── frontend/
├── terraform/
├── docker-compose.yml
├── Jenkinsfile
├── .env
└── README.md
```

---

# DevOps Concepts Demonstrated

This project showcases a complete cloud deployment workflow using AWS and modern DevOps practices.

- Docker containerization
- Docker Compose orchestration
- Amazon EC2 deployment
- Amazon RDS PostgreSQL
- Amazon S3 object storage
- Infrastructure as Code with Terraform
- CI/CD using Jenkins
- GitHub version control
- Environment-based configuration
- Full-stack cloud deployment

---

# License

This project was developed as a DevOps portfolio project to demonstrate cloud deployment, infrastructure provisioning, and CI/CD automation using AWS.
