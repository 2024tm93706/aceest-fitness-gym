# ACEest Fitness & Gym DevOps Pipeline

## 📌 Overview
This project demonstrates a complete CI/CD pipeline using Flask, Docker, GitHub Actions, and Jenkins.

---

## 🏗️ Architecture
Local Development → GitHub → GitHub Actions (CI) → Docker → Jenkins Build Validation

---

## 🚀 Features
- REST API using Flask
- Automated testing with Pytest
- Docker containerization
- CI pipeline with GitHub Actions
- Jenkins build integration

---

## 🛠️ Local Setup

```bash
git clone <repo-url>
cd aceest-fitness-gym
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/app.py