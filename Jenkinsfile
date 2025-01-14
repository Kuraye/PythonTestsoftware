pipeline {
    agent any

    environment {
        PYTHON_HOME = '/usr/bin/python3'
        PIP_HOME = '/usr/bin/pip3'
        VENV_DIR = 'venv'
        MY_VAR = 'This is a test variable' 
    }

    stages {
        stage('Test Variable Substitution') {
            steps {
                script {
                    sh '''
                        /bin/bash -c "
                            echo \"MY_VAR: \${MY_VAR}\" 
                        "
                    '''
                }
            }
        }

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
                        cat /var/jenkins_home/workspace/Python Pipeline@tmp/durable-c9375f2d/script.sh.copy
                        /bin/bash -c "
                            cat /var/jenkins_home/workspace/Python Pipeline@tmp/durable-c9375f2d/script.sh.copy  # Print the script content
                            echo PYTHON_HOME: \${PYTHON_HOME}
                            \${PYTHON_HOME} -m venv \$VENV_DIR
                            source \$VENV_DIR/bin/activate
                            pip install flask flask-wtf wtforms werkzeug flask-session splitter PyPDF2 pytest pylint
                            sleep 60 
                        "
                    '''
                }
            }
        }

        stage('Run Linter') {
            steps {
                script {
                    sh '''
                        /bin/bash -c "
                            source \$VENV_DIR/bin/activate
                            export PATH="\${env.WORKSPACE}/venv/bin:\$PATH"
                            pylint PythonTestSoftware/
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
                            source \$VENV_DIR/bin/activate
                            pytest --junitxml=report.xml
                        "
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
