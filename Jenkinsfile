pipeline {
    agent any

    environment {
        VENV = "${WORKSPACE}/venv"
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
        stage('Deploy') {
            steps {
                echo 'deploying application'
                // Add your deployment steps here
            }
        }
    }

    post {
        always {
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