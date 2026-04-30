pipeline {
    agent any

    environment {
        IMAGE = "2024tm93706/aceest-fitness-gym"
    }

    stages {

        stage('Install & Test') {
            steps {
                sh '''
                apt-get update
                apt-get update
                apt-get install -y python3 python3-pip python3-venv curl

                # install kubectl
                curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl"
                install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                pytest
                '''
            }
        }

        stage('Build Docker') {
            steps {
                sh 'docker build -t $IMAGE:$BUILD_NUMBER -f docker/Dockerfile .'
            }
        }

        stage('Login to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                }
            }
        }

        stage('Push Docker') {
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
