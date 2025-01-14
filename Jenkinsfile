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
          echo PYTHON_HOME: /usr/bin/python3
          # Check if PYTHON_HOME is set and executable
          if [[ -x /usr/bin/python3 ]]; then
            /usr/bin/python3 -m venv $VENV_DIR  # Use $VENV_DIR variable
          else
            echo ERROR: PYTHON_HOME is not set or not executable.
            exit 1
          fi
          source $VENV_DIR/bin/activate
          pip install flask flask-wtf wtforms werkzeug flask-session splitter PyPDF2 pytest pylint
          '''
        }
      }
    }

    stage('Run Linter') {
      steps {
        script {
          sh '''
          source "$VENV_DIR/bin/activate"
          export PATH="$VENV_DIR/bin:$PATH"
          pylint PythonTestSoftware/  # Removed trailing space
          '''
        }
      }
    }

    stage('Run Tests') {
      steps {
        script {
          sh '''
          /bin/bash -c "
          source \$VENV_DIR/bin/activate
          pytest --junitxml=report.xml
          "
          '''
        }
      }
      post {
        always {
          junit 'report.xml'
          parseClassicLog rules: [
            [
              ruleName: 'Bad Substitution',
              ruleExpression: '.*script.sh.copy: 2: .*',
              category: 'Error',
              severity: 'High'
            ]
          ]
        }
      }
    }
  }
}
