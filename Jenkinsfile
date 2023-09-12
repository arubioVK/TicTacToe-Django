      pipeline {
        agent {
            docker { image 'python:3.11' }
        }
        stages {
            stage('Build') {
                steps {
                    sh 'pip install -r django/requirements.txt'
                }
            }

            stage('Test') {
                steps {
                    sh 'python django/manage.py test ./django'
                }
            }

            stage('Deploy') {
                steps {
                    sh 'echo not yet...'
                }
            }
        }
    }
