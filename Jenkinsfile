pipeline {

    agent any

    stages {

        
        stage('Setup') {
    steps {
        bat 'where python'
        bat 'python --version'

        bat 'if exist reports rmdir /s /q reports'
        bat 'mkdir reports'

        bat '"C:\\Users\\neera\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" -m venv .venv'
        bat '.venv\\Scripts\\python -m pip install -r requirements.txt'
        bat '.venv\\Scripts\\python -m playwright install'
    }
}

        stage('Start Application') {
            steps {
                bat 'start /B .venv\\Scripts\\python app\\web\\app.py'
            }
        }

        stage('Wait for Application') {
            steps {
                bat '.venv\\Scripts\\python scripts\\wait_for_app.py'
            }
        }

        stage('Test') {
            steps {
                bat '''
                    .venv\\Scripts\\python -m pytest framework/tests ^
                    --junitxml=reports\\test-results.xml ^
                    --html=reports\\report.html ^
                    --self-contained-html
                '''
            }
        }
    }

    post {
        always {
            junit 'reports/test-results.xml'

            publishHTML(target: [
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Playwright HTML Report',
                keepAll: true,
                alwaysLinkToLastBuild: true,
                allowMissing: false
            ])
        }
    }
}