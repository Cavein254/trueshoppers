pipeline {
    agent any

    environment {
        VENV = "${WORKSPACE}/venv"
        DOCKER_IMAGE = 'cave254/trueshoppers'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        DOCKERHUB_CREDENTIALS = credentials('dockerhub_auth') // Replace with your Jenkins credentials ID
        DB_NAME='mydatabase'
        DB_USER='myuser'
        DB_PASSWORD='mysecretpassword'
        DB_HOST='192.168.122.200'
        DB_PORT='32345'
    }

    stages {
        stage('setup') {
            steps {
               echo "setting up python env"
                // install python3-venv if you don't have it
                sh 'python3 -m pip install --upgrade pip'

                // create a virtual environment if it doesn't exist
                sh '''
                if [ ! -d "$VENV" ]; then
                    python3 -m venv venv
                fi
                '''

                // activate the virtual environment and install dependencies
                sh '''
                . ${VENV}/bin/activate
                pip install -r requirements-dev.txt
                '''
            }
        }
        stage('Build') {
            steps {
                echo 'collecting static files and preparing build'
                sh '''
                . ${VENV}/bin/activate
                python manage.py collectstatic --noinput --settings=core.settings.dev
                python manage.py migrate --settings=core.settings.dev
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'running tests'
                sh '''
                . ${VENV}/bin/activate
                python manage.py test --settings=core.settings.dev
                '''
            }
        }
        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                sh '''
                docker build \
                --build-arg DJANGO_SETTINGS_MODULE=core.settings.prod \
                -f Dockerfile.prod -t ${DOCKER_IMAGE}:${IMAGE_TAG} .
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
                docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
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
