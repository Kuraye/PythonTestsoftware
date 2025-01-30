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
            bash ''' # Use bash step
                #!/bin/bash
                echo "PYTHON_HOME: $PYTHON_HOME"
                if [[ -x "$PYTHON_HOME" ]]; then # Now this will work
                    virtualenv --python="$PYTHON_HOME" "$VENV_DIR"
                else
                    echo "ERROR: PYTHON_HOME is not set or not executable."
                    exit 1
                fi
                source "$VENV_DIR/bin/activate"
                pip install flask flask-wtf wtforms werkzeug flask-session splitter PyPDF2 pytest pylint
            '''
            }
        }
    }
    stage('Run Linter') {
      steps {
        script {
          sh '''
          #!/bin/bash
          source "$VENV_DIR/bin/activate"
          export PATH="$VENV_DIR/bin:$PATH"
          pylint PythonTestSoftware/
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
          #!/bin/bash
          source "$VENV_DIR/bin/activate"
          python PythonTestSoftware/main.py 
          '''
        }
      }
    }

    stage('Run Tests') {
      steps {
        script {
          sh '''
          #!/bin/bash
          source "$VENV_DIR/bin/activate"
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
  }
}
