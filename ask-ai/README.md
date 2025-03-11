# Ask-AI Project

This project provides a set of services for our Ask-AI system, including local development orchestration via Docker and Kubernetes deployment configurations.

## Directory Structure

- **docker-compose.yml**: Service orchestration for local development.
- **kubernetes/**: Kubernetes deployment configurations.
  - **ingestion.yaml**: Deployment for the Ingestion Service.
  - **knowledge-representation.yaml**: Deployment for the Knowledge Representation Service.
  - **query-processing.yaml**: Deployment for the Query Processing Service.
  - **response-generation.yaml**: Deployment for the Response Generation Service.
  - **security.yaml**: Deployment for the Security Service.
  - **monitoring.yaml**: Deployment for the Monitoring Service.
- **requirements.txt**: Python dependencies.
- **src/**: Source code directory.

## Getting Started

### Local Development

To get started with local development using Docker Compose, run:
```bash
docker-compose up --build
```

### Kubernetes Deployment

Apply the Kubernetes configurations by running:
```bash
kubectl apply -f kubernetes/
```

## Requirements

Install the required Python dependencies using:
```bash
pip install -r requirements.txt
```

## Source Code

All source code for the Ask-AI services can be found in the **src/** directory.
