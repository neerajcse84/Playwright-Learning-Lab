pipeline {

    agent any

    stages {

        
        stage('Setup') {
    steps {
       
        bat 'if exist reports rmdir /s /q reports'
        bat 'mkdir reports'

        bat '"C:\\Users\\neera\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" -m venv .venv'
        bat '.venv\\Scripts\\python -m pip install -r requirements.txt'
        bat '.venv\\Scripts\\python -m playwright install'
    }
}

        stage('Start Application') {
            steps {
                bat 'set APP_PORT=5000 && start /B .venv\\Scripts\\python app\\web\\app.py'
            }
        }

        stage('Wait for Application') {
            steps {
                bat 'set APP_URL=http://127.0.0.1:5000 && .venv\\Scripts\\python scripts\\wait_for_app.py'
            }
        }

        stage('Test') {
            steps {
                bat '''
                    .venv\\Scripts\\python -m pytest framework/tests -m "not deployment_smoke" ^
                    --junitxml=reports\\test-results.xml ^
                    --html=reports\\report.html ^
                    --self-contained-html
                '''
            }
        }

       stage('Package') {
    steps {
        bat 'if not exist artifacts mkdir artifacts'
        bat 'tar -a -c -f artifacts\\flask-app.zip app requirements.txt'
    }
}
    stage('Deploy') {
    steps {
        bat 'if not exist C:\\Deploy\\Playwright-Learning-Lab mkdir C:\\Deploy\\Playwright-Learning-Lab'
        bat 'copy /Y artifacts\\flask-app.zip C:\\Deploy\\Playwright-Learning-Lab\\'
        bat 'tar -xf C:\\Deploy\\Playwright-Learning-Lab\\flask-app.zip -C C:\\Deploy\\Playwright-Learning-Lab'
    }
}

    stage('Prepare Deployment Runtime') {
    steps {
        bat '"C:\\Users\\neera\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" -m venv C:\\Deploy\\Playwright-Learning-Lab\\.venv'

        bat 'C:\\Deploy\\Playwright-Learning-Lab\\.venv\\Scripts\\python -m pip install -r C:\\Deploy\\Playwright-Learning-Lab\\requirements.txt'
    }
}
    stage('Start Deployed Application') {
    steps {
        bat 'set APP_PORT=5001 && start /B C:\\Deploy\\Playwright-Learning-Lab\\.venv\\Scripts\\python C:\\Deploy\\Playwright-Learning-Lab\\app\\web\\app.py'
        
    }
}
    stage('Wait for Deployed Application') {
    steps {
        bat 'set APP_URL=http://127.0.0.1:5001 && C:\\Deploy\\Playwright-Learning-Lab\\.venv\\Scripts\\python scripts\\wait_for_app.py'
    }
}
    stage('Smoke Test') {
    steps {
        bat 'set APP_URL=http://127.0.0.1:5001 && C:\\Deploy\\Playwright-Learning-Lab\\.venv\\Scripts\\python -m pytest framework\\tests\\test_smoke.py -m deployment_smoke -v'
    }
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
            archiveArtifacts artifacts: 'artifacts/flask-app.zip', fingerprint: true
        }
        
    }
