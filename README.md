![CI](https://github.com/2024tm93706/aceest-fitness-gym/actions/workflows/main.yml/badge.svg)

# ACEest Fitness & Gym DevOps Pipeline

## Overview
This project demonstrates a complete CI/CD pipeline using Flask, Docker, GitHub Actions, and Jenkins.

---

## Architecture
Local Development → GitHub → GitHub Actions (CI) → Docker → Jenkins Build Validation

---

## Features
- REST API using Flask
- Automated testing with Pytest
- Docker containerization
- CI pipeline with GitHub Actions
- Jenkins build integration

---

## Local Setup

```bash
git clone https://github.com/2024tm93706/aceest-fitness-gym
cd aceest-fitness-gym
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/app.py
```

## Run Tests

```bash
python -m pytest
```

## Docker Usage

```bash
docker build -t aceest-gym .
docker run -p 5001:5000 aceest-gym
```
## CI/CD Pipeline 

The GitHub Actions pipeline is triggered on every push and pull request. It performs:
	•	Dependency installation
	•	Running unit tests
	•	Docker image build

## Jenkins Integration

Jenkins is configured to:
	•	Pull latest code from GitHub
	•	Build Docker image
	•	Validate build success

## Pipeline Flow
Every code push automatically triggers testing and Docker build via GitHub Actions, followed by Jenkins build validation.

## Screenshots 

# App running within docker
<img width="1326" height="459" alt="Screenshot 2026-04-02 at 12 08 34 PM" src="https://github.com/user-attachments/assets/e31b9802-b6cf-4d75-ae99-17fd38186e72" />
<img width="433" height="122" alt="Screenshot 2026-04-02 at 12 05 47 PM" src="https://github.com/user-attachments/assets/f4014eda-d88d-493a-8fe3-a50aa8226914" />

# Github actions success 
<img width="1340" height="238" alt="Screenshot 2026-04-02 at 12 06 49 PM" src="https://github.com/user-attachments/assets/b62f3bdf-3392-4b1c-bf18-61529cd41fbd" />
<img width="1198" height="752" alt="Screenshot 2026-04-02 at 12 07 26 PM" src="https://github.com/user-attachments/assets/490b5811-84a0-4faa-b2e0-2f8dfa555226" />
<img width="1202" height="899" alt="Screenshot 2026-04-02 at 12 07 12 PM" src="https://github.com/user-attachments/assets/aa981142-ee8f-4740-85bf-e487ecd26308" />


# Jenkins success
<img width="773" height="366" alt="Screenshot 2026-04-02 at 12 04 17 PM" src="https://github.com/user-attachments/assets/c0b478bc-4137-4482-9729-8132fd2c26e8" />
<img width="1030" height="214" alt="Screenshot 2026-04-02 at 12 04 03 PM" src="https://github.com/user-attachments/assets/9e120eb0-4956-4cb6-ad0b-dfe87006da12" />

