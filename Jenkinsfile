pipeline {
    agent any

    environment {
        VENV = "${WORKSPACE}/venv"
        DOCKER_IMAGE = 'cave254/trueshoppers'
        BUILD_TAG = "${env.BUILD_NUMBER}"
        DOCKERHUB_CREDENTIALS = credentials('dockerhub_auth') // Replace with your Jenkins credentials ID
    }

    stages {
        stage('setup') {
            steps {
               echo "setting up python env"
                // install python3-venv if you don't have it
                sh 'python3 -m pip install --upgrade pip'
                sh 'python3 -m pip install virtualenv'

                // create a virtual environment if it doesn't exist
                sh '''
                if [ ! -d "$VENV" ]; then
                    python3 -m venv venv
                fi
                '''

                // activate the virtual environment and install dependencies
                sh '''
                source ${VENV}/bin/activate
                pip install -r requirements.txt
                '''
            }
        }
        stage('Build') {
            steps {
                echo 'collecting static files and preparing build'
                sh '''
                source ${VENV}/bin/activate
                python manage.py collectstatic --noinput
                python manage.py migrate
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'running tests'
                sh '''
                source ${VENV}/bin/activate
                python manage.py test
                '''
            }
        }
        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                sh '''
                docker build -t ${DOCKER_IMAGE}:${BUILD_TAG} .
                '''
            }
        
        }
        stage('Docker Login') {
            steps {
                echo 'Logging into Docker Hub...'
                sh '''
                echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
                '''
            }
        }
        stage('Docker Push') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                sh '''
                docker push ${DOCKER_IMAGE}:${BUILD_TAG}
                '''
            }
        }
    }

    post {
        always {
            echo 'docker logout'
            sh 'docker logout'
            echo 'Cleaning up...'
            sh 'deactivate || true'
            sh 'rm -rf ${VENV}'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}