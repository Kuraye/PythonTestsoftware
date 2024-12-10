pipeline {
  agent any
  tools {
    python '3.9.1'
  }
  stages {
    stage('Clean Workspace') {
      steps {
        cleanWs()
      }
    }

    stage('Checkout') {
      steps {
        git url: 'https://github.com/Kuraye/PythonTestsoftware.git'
      }
    }

    stage('Install Dependencies') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }

    stage('Build') {
      steps {
        sh 'python build.py' // Replace with your actual build script
      }
    }

    stage('Test') {
      steps {
        sh 'pytest' // Adjust with pytest options if needed
      }
    }

    stage('Deploy to Container') {
      steps {
        script {
          // Replace with your specific container deployment steps
          // (e.g., using Docker or other container orchestration tools)
          echo 'Deploying...'
        }
      }
    }
  }
}
