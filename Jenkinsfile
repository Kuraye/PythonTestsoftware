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
                        cat script.sh.copy > script_content.log
                        /bin/bash -c "
                            echo \"PYTHON_HOME: \${PYTHON_HOME}\"
                            \${PYTHON_HOME} -m venv \$VENV_DIR
                            source \$VENV_DIR/bin/activate
                            pip install flask flask-wtf wtforms werkzeug flask-session splitter PyPDF2 pytest pylint
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
