pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Images') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Start Containers') {
            steps {
                sh 'docker compose up -d'
            }
        }

        stage('Wait') {
            steps {
                sh 'sleep 40'
            }
        }

        stage('Backend Health Check') {
            steps {
                sh '''
                curl --fail http://localhost:8000/docs > /dev/null
                '''
            }
        }

        stage('Frontend Check') {
            steps {
                sh '''
                curl --fail http://localhost:5173 > /dev/null || true
                '''
            }
        }
    }

    post {
        always {
            sh 'docker compose down'
        }
    }
}
