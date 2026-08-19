pipeline {

    agent any

    environment {
        APP_IMAGE       = "playwright-lab:${BUILD_NUMBER}"
        TEST_IMAGE      = "playwright-test:${BUILD_NUMBER}"
        APP_CONTAINER   = "playwright-flask-${BUILD_NUMBER}"
        NETWORK_NAME    = "qa-network-${BUILD_NUMBER}"
        APP_URL         = "http://playwright-flask-${BUILD_NUMBER}:5000"
        HOST_PORT       = "5000"
    }

    stages {

        stage('Check Docker') {
    steps {
        bat 'docker --version'
        bat 'docker info'
    }
}

        stage('Build App Image') {
            steps {
                bat 'docker build -t %APP_IMAGE% .'
            }
        }

        stage('Build Test Image') {
            steps {
                bat 'docker build -f Dockerfile.test -t %TEST_IMAGE% .'
            }
        }

        stage('Create Docker Network') {
            steps {
                bat 'docker network create %NETWORK_NAME%'
            }
        }

        stage('Start Application Container') {
            steps {
                bat '''
                    docker run -d ^
                    --name %APP_CONTAINER% ^
                    --network %NETWORK_NAME% ^
                    -e APP_PORT=5000 ^
                    -p %HOST_PORT%:5000 ^
                    %APP_IMAGE%
                '''
            }
        }

        stage('Wait for Application') {
            steps {
                bat '''
                    set APP_URL=http://127.0.0.1:%HOST_PORT% && ^
                    C:\\Users\\neera\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe ^
                    scripts\\wait_for_app.py
                '''
            }
        }

        stage('Run Tests in Docker') {
            steps {
                bat '''
                    docker run --rm ^
                    --network %NETWORK_NAME% ^
                    -e BASE_URL=%APP_URL% ^
                    -e HEADLESS=true ^
                    -v "%WORKSPACE%:/tests" ^
                    -w /tests ^
                    %TEST_IMAGE% ^
                    pytest framework/tests -m "not deployment_smoke" ^
                    --junitxml=reports\\test-results.xml ^
                    --html=reports\\report.html ^
                    --self-contained-html ^
                    -v
                '''
            }
        }

        stage('Package Application') {
            steps {
                bat 'if not exist artifacts mkdir artifacts'
                bat 'tar -a -c -f artifacts\\flask-app.zip app requirements.txt Dockerfile'
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
                allowMissing: true
            ])
        }

        success {
            archiveArtifacts artifacts: 'artifacts/flask-app.zip',
                               fingerprint: true
        }

        cleanup {
            bat 'docker rm -f %APP_CONTAINER% 2>nul || exit /b 0'
            bat 'docker network rm %NETWORK_NAME% 2>nul || exit /b 0'
        }
    }
}