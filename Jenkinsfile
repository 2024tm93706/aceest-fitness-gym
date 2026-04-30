pipeline {
    agent any

    environment {
        IMAGE_NAME = "aceest-fitness-gym:latest"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Image (Minikube Docker)') {
            steps {
                sh '''
                echo "Switching to Minikube Docker..."
                eval $(minikube docker-env)

                echo "Building Docker image..."
                docker build -t $IMAGE_NAME -f docker/Dockerfile .
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                echo "Deploying to Kubernetes..."

                kubectl apply -f k8s/

                echo "Updating deployment image..."
                kubectl set image deployment/aceest-green aceest-container=$IMAGE_NAME || true

                echo "Deployment complete"
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                echo "Checking pods..."
                kubectl get pods

                echo "Checking services..."
                kubectl get svc
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully 🚀'
        }
        failure {
            echo 'Pipeline failed ❌'
        }
    }
}