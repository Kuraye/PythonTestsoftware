pipeline {
    agent {
        // Use a Python Docker image as the build agent
        docker { image 'python:3.10.16' }
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Checkout code from GitHub
                git url: 'https://github.com/Kuraye/PythonTestsoftware.git', branch: 'main'
            }
        }

        stage('Set Up Python Environment') {
            steps {
                script {
                    // Install required Python packages
                    sh '''
                        pip3 install --upgrade pip
                        pip3 install flask
                        pip3 install flask-wtf
                        pip3 install wtforms
                        pip3 install werkzeug
                        pip3 install flask-session
                        pip3 install splitter
                        pip3 install creator
                    '''
                }
            }
        }

        stage('Run Application') {
            steps {
                // Run the application
                sh 'python3 app.py'
            }
        }
    }

    post {
        always {
            // Clean up workspace
            cleanWs()
        }
    }
}

