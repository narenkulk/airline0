pipeline {
  agent { docker { image 'python:3.8' } }
  stages {
    stage('build') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }
    stage('test') {
      steps {
        sh 'python3 manage.py test'
      }   
    }
  }
}