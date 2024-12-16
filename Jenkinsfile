pipeline {
    agent any

    environment {
        PYTHON_HOME = '/usr/bin/python3'
        PIP_HOME = '/usr/bin/pip3'
        VENV_DIR = 'venv'  // Virtual environment directory path
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
                        # Use bash shell to ensure virtual environment setup
                        /bin/bash -c "
                            $PYTHON_HOME -m venv $VENV_DIR  # Create a virtual environment
                            source $VENV_DIR/bin/activate   # Activate the virtual environment
                            pip install --upgrade pip  # Upgrade pip
                            pip install flask flask-wtf wtforms werkzeug flask-session splitter  # Install required packages
                        "
                    '''
                }
            }
        }

        stage('Run Application') {
            steps {
                script {
                    // Activate the virtual environment and run Flask app in the background
                    sh '''
                        /bin/bash -c "
                            source $VENV_DIR/bin/activate  # Activate the virtual environment
                            nohup python main.py &  # Run Flask app in the background
                        "
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()  // Clean the workspace after the pipeline finishes
        }
    }
}
