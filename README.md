# 🧠 Mental Health Score Prediction App


[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/lambda/)

A full-stack machine learning web application that predicts mental health scores based on user lifestyle data. Built with **FastAPI**, **Pandas**, and **Scikit-Learn**, and deployed serverlessly using **AWS Lambda** and **Amazon ECR**.


[🚀 Live Demo](#-live-demo) • [📐 Architecture](#-system-architecture) • [📦 Deployment Guide](#-deployment-guide)

---

## 🚀 Features
* **Machine Learning Backend:** Powered by a trained Scikit-Learn pipeline using demographic and behavioral metrics.
* **Interactive UI:** Clean, responsive web interface served directly via FastAPI static mounts.
* **Serverless Architecture:** Deployed on AWS Lambda for a cost-efficient, scale-to-zero setup ($0 when idle).

---

## 🛠️ Tech Stack
* **Python & FastAPI:** High-performance web framework and API routing.
* **Scikit-Learn & Pandas:** Data preprocessing and machine learning inference.
* **Docker & Amazon ECR:** Containerization and image registry.
* **AWS Lambda & Mangum:** Serverless execution environment.

---

## 📐 System Architecture

```mermaid
flowchart TD
    subgraph Client ["Client Layer"]
        A[User / Browser] -->|1. Triggers Function URL| B(HTTP Request / UI Action)
    end

    subgraph AWS_Lambda ["AWS Serverless Compute (Scale-to-Zero)"]
        B -->|2. Event Invocation| C{Container State?}
        C -->|Cold Start / Idle| D[Pull 2GB Docker Image from ECR]
        C -->|Warm Start / Active| E[Reuse Active Execution Context]
        D --> F[Initialize FastAPI & Load .pkl Pipeline]
        E --> F
        F --> G[Serve Frontend UI & Route API Endpoints]
    end

    subgraph ML_Engine ["Inference Engine"]
        G -->|3. Send POST Data| H[Pandas Feature Preprocessing]
        H -->|4. Vectorize Data| I[Scikit-Learn Pipeline Inference]
        I -->|5. Compute Score| G
    end

    G -->|6. JSON Prediction / HTML Response| A

    style A fill:#4F46E5,stroke:#fff,stroke-width:2px,color:#fff
    style C fill:#F59E0B,stroke:#fff,stroke-width:2px,color:#fff
    style F fill:#3B82F6,stroke:#fff,stroke-width:2px,color:#fff
    style I fill:#10B981,stroke:#fff,stroke-width:2px,color:#fff
```


## 📁 Project Structure
```text
mental-health-app/
├── model/
│   └── mental_health_pipeline.pkl
├── static/
│   ├── index.html
│   ├── style.css
│   └── script_2.js
├── .dockerignore
├── Dockerfile
├── main.py
└── requirements.txt
```

---

## ⚙️ Prerequisites
Before running or deploying the app, ensure you have:
* [Docker Desktop](https://www.docker.com/) installed and running.
* [AWS CLI](https://aws.amazon.com/cli/) configured with your credentials (`aws configure`).

---

## 📦 Deployment Guide (AWS Lambda + ECR)

### 1. Build the Docker Image
To ensure compatibility with AWS Lambda, build the container image while explicitly disabling provenance metadata:
```bash
docker build --provenance=false -t mental-health-app .
```

### 2. Authenticate with AWS ECR
Log in to your AWS Elastic Container Registry (replace `<your-region>` and `<your-account-id>`):
```bash
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com
```

### 3. Tag and Push the Image
Tag your local image and push it to your ECR repository:
```bash
docker tag mental-health-app:latest <your-account-id>.dkr.ecr.<your-region>[.amazonaws.com/mental-health-app:latest](https://.amazonaws.com/mental-health-app:latest)

docker push <your-account-id>.dkr.ecr.<your-region>[.amazonaws.com/mental-health-app:latest](https://.amazonaws.com/mental-health-app:latest)
```

### 4. Configure AWS Lambda
1. Open the **AWS Lambda Console** and click **Create function**.
2. Select **Container image**, name your function, and browse to select your ECR image.
3. Under **Advanced settings**:
   * Enable **Function URL**.
   * Set **Auth type** to **`NONE`**.
   * Check the **CORS** box.
4. Click **Create function**.

### 5. Update Resource Settings
Because machine learning libraries (`pandas` and `scikit-learn`) require sufficient memory to initialize:
1. Go to your Lambda function's **Configuration** tab.
2. Select **General configuration** -> **Edit**.
3. Set **Memory** to **1024 MB**.
4. Set **Timeout** to **30 seconds**.
5. Click **Save**.

🎉 **You're done!** Open your Lambda Function URL to view and test your application live.
