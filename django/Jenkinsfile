      pipeline {
        agent {
            docker { image 'python:3.11' }
        }
        stages {
            stage('Build') {
                steps {
                    sh 'pip install -r requirements.txt'
                }
            }

            stage('Test') {
                steps {
                    sh 'python manage.py test'
                }
            }

            stage('Deploy') {
                steps {
                    sh 'echo not yet...'
                }
            }
        }
    }
