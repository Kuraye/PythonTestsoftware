pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                // Checkout code from the GitHub repository
                git url: 'https://github.com/Kuraye/PythonTestsoftware.git', branch: 'main'
            }
        }

        stage('Set Up Python Environment') {
            steps {
                script {
                    // Ensure Python3 and pip3 are installed
                    sh '''
                        if ! command -v python3 &> /dev/null; then
                            echo "Installing Python3"
                            sudo apt-get update
                            sudo apt-get install -y python3
                        fi

                        if ! command -v pip3 &> /dev/null; then
                            echo "Installing pip3"
                            sudo apt-get install -y python3-pip
                        fi
                    '''
                    
                    // Install required Python packages
                    sh '''
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
                // Run the application (adjust the entry point file as needed)
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

