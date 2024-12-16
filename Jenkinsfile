pipeline {
    agent any

    environment {
        PYTHON_HOME = '/usr/bin/python3'
        PIP_HOME = '/usr/bin/pip3'
        VENV_DIR = 'venv'  // Virtual environment directory path
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()  // Clean the workspace at the start of the pipeline
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
                        /bin/bash -c "
                            $PYTHON_HOME -m venv $VENV_DIR  # Create a virtual environment
                            source $VENV_DIR/bin/activate   # Activate the virtual environment
                            pip install --upgrade pip  # Upgrade pip
                            pip install flask flask-wtf wtforms werkzeug flask-session splitter PyPDF2 pytest
                        "
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh '''
                        /bin/bash -c "
                            source $VENV_DIR/bin/activate
                            pytest --junitxml=report.xml
                        "
                    '''
                }
            }
            post {
                always {
                    junit 'report.xml'  // Publish the test results
                }
            }
        }
    }
}
