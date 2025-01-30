pipeline {
  agent any

  environment {
    PYTHON_HOME = '/usr/bin/python3'
    PIP_HOME = '/usr/bin/pip3'
    VENV_DIR = 'venv'
  }

  stages {
    stage('Clean Workspace') {
      steps {
        cleanWs()
      }
    }

    stage('Clone Repository') {
      steps {
        git url: 'https://github.com/Kuraye/PythonTestsoftware.git', branch: 'main'
      }
    }

    stage('Set Up Python Environment') {
      steps {
        script {
          sh '''
          echo "PYTHON_HOME: $PYTHON_HOME"
          if [ -x "$PYTHON_HOME" ]; then
              python3 -m venv "$VENV_DIR"
          else
              echo "ERROR: PYTHON_HOME is not set or not executable."
              exit 1
          fi
          . "$VENV_DIR/bin/activate"
          pip install flask flask-wtf wtforms werkzeug flask-session splitter PyPDF2 pytest pylint
          '''
        }
      }
    }

    stage('Run Linter') {
      steps {
        script {
          sh '''
          #!/bin/sh
          . "$VENV_DIR/bin/activate"
          export PATH="$VENV_DIR/bin:$PATH"
          pylint *.py || true
          '''
        }
      }
      post {
        always {
          archiveArtifacts artifacts: '**/pylint_output.txt', allowEmptyArchive: true
        }
      }
    }

    stage('Run Application') {
      steps {
        script {
          sh '''
          . "$VENV_DIR/bin/activate"
          nohup python main.py & 
          echo $! > flask_pid.txt
          '''
        }
      }
    }

    stage('Run Tests') {
      steps {
        script {
          sh '''
          . "$VENV_DIR/bin/activate"
          pytest --junitxml=report.xml
          '''
        }
      }
      post {
        always {
          junit 'report.xml'
        }
      }
    }

    stage('Stop Flask Application') {
      steps {
        script {
          sh '''
          kill $(cat flask_pid.txt) || true
          '''
        }
      }
    }
  }
}
