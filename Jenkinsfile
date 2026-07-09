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

        stage('Wait for Startup') {
            steps {
                sh 'sleep 15'
            }
        }

        stage('Verify Backend') {
            steps {
                sh '''
                docker exec Backend curl --fail http://localhost:8000/docs
                '''
            }
}

        stage('Verify Frontend') {
            steps {
                sh '''
                docker exec Frontend wget --spider http://localhost:5173
                '''
            }
}

    post {
        always {
            sh 'docker compose logs'
            sh 'docker compose down -v'
        }
    }
}
