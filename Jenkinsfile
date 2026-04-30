pipeline {
    agent any

    environment {
        IMAGE = "2024tm93706/aceest-fitness-gym"
    }

    stages {

        stage('Clean') {

            steps {

                deleteDir()

            }

        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh '''
                docker build -t $IMAGE:test -f docker/Dockerfile .
                docker run --rm $IMAGE:test pytest
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
                /usr/local/bin/kubectl set image deployment/aceest-green aceest-container=$IMAGE:$BUILD_NUMBER || true
                /usr/local/bin/kubectl apply -f k8s/ --validate=false
                '''
            }
        }
    }
}
