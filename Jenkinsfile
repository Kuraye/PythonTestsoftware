pipeline {
    agent any

    environment {       
        PYTHON_HOME = '/usr/bin/python3'  
        PIP_HOME = '/usr/bin/pip3'  
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/Kuraye/PythonTestsoftware.git', branch: 'main'
            }
        }

        stage('Set Up Python Environment') {
            steps {
                script {
                    sh '''
                        $PYTHON_HOME -m venv venv  # Create a virtual environment
                        source venv/bin/activate   # Activate the virtual environment
                        pip install --upgrade pip  # Upgrade pip
                        pip install flask flask-wtf wtforms werkzeug flask-session splitter creator  # Install required packages
                    '''
                }
            }
        }

        stage('Run Application') {
            steps {
                sh '''
                    source venv/bin/activate  # Activate the virtual environment
                    python3 app.py  # Run your Python application
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
