pipeline {
    agent any

    environment {
        DOCKER_USER = credentials('docker_user')   // Jenkins credential ID for Docker username
        DOCKER_PASS = credentials('docker_pass')   // Jenkins credential ID for Docker password
    }

    stages {
        stage('Dev') {
            when {
                allOf {
                    anyOf {
                        branch 'develop'
                    }
                    anyOf {
                        triggeredBy 'SCMTrigger'   // handles push
                        triggeredBy 'PullRequestSCMTriggerCause' // handles PR
                    }
                }
            }
            agent {
                docker {
                    image 'python:3.12-slim'
                    args '-u root'
                }
            }
            environment {
                DJANGO_SETTINGS_MODULE = 'core.settings.dev'
            }
            steps {
                sh '''
                  python -m venv venv
                  . venv/bin/activate
                  pip install --upgrade pip
                  pip install -r requirements.txt
                  python manage.py migrate
                  python manage.py test
                '''
            }
        }

        stage('Test') {
            when {
                allOf {
                    anyOf {
                        branch 'main'
                        branch 'develop'
                    }
                    anyOf {
                        triggeredBy 'SCMTrigger'
                        triggeredBy 'PullRequestSCMTriggerCause'
                    }
                }
            }
            agent {
                docker {
                    image 'python:3.12-slim'
                    args '-u root'
                }
            }
            environment {
                DJANGO_SETTINGS_MODULE = 'core.settings.test'
            }
            steps {
                sh '''
                  python -m venv venv
                  . venv/bin/activate
                  pip install --upgrade pip
                  pip install -r requirements.txt
                  python manage.py migrate
                  python manage.py test
                '''
            }
        }

        stage('Deploy') {
            when {
                allOf {
                    branch 'main'
                    triggeredBy 'SCMTrigger'   // only pushes, not PRs
                }
            }
            agent {
                docker {
                    image 'docker:latest'
                    args '--privileged -v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                sh '''
                  echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                  docker build -t myapp:${GIT_COMMIT} .
                  docker push myapp:${GIT_COMMIT}
                '''
            }
        }
    }
}
