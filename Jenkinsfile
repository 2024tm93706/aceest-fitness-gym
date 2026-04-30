pipeline {
    agent any

    environment {
        IMAGE = "2024tm93706/aceest-fitness-gym"
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/2024tm93706/aceest-fitness-gym.git'
            }
        }

        stage('Install & Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE:$BUILD_NUMBER -f docker/Dockerfile .'
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push $IMAGE:$BUILD_NUMBER'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                kubectl set image deployment/aceest-green aceest-container=$IMAGE:$BUILD_NUMBER || true
                kubectl apply -f k8s/
                '''
            }
        }
    }
}