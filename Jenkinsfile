pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    parameters {
        choice(name: 'BROWSER', choices: ['chrome', 'firefox', 'edge'], description: 'Browser to run tests')
        booleanParam(name: 'HEADLESS', defaultValue: true, description: 'Run in headless mode')
        string(name: 'TEST_PATH', defaultValue: 'tests', description: 'Path to tests')
        string(name: 'MARKERS', defaultValue: '', description: 'Test markers (e.g., smoke)')
        string(name: 'PARALLEL_WORKERS', defaultValue: '4', description: 'Number of parallel workers')
    }

    stages {
        stage('Setup') {
            steps {
                sh 'apt-get update && apt-get install -y docker.io docker-compose'
                sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Start Selenium Grid') {
            steps {
                sh 'docker-compose up -d selenium-hub chrome firefox edge'
                sh 'sleep 10' // Wait for Grid to be ready
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def markerArg = params.MARKERS ? "-m ${params.MARKERS}" : ""

                    sh """
                    BROWSER=${params.BROWSER} \
                    HEADLESS=${params.HEADLESS} \
                    USE_GRID=true \
                    PARALLEL_WORKERS=${params.PARALLEL_WORKERS} \
                    pytest ${params.TEST_PATH} -v -n ${params.PARALLEL_WORKERS} ${markerArg} \
                    --alluredir=reports/allure-results
                    """
                }
            }
        }

        stage('Generate Reports') {
            steps {
                sh 'allure generate reports/allure-results -o reports/allure-report --clean'
            }
            post {
                always {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'reports/allure-results']]
                    ])
                }
            }
        }
    }

    post {
        always {
            sh 'docker-compose down'
            cleanWs()
        }
    }
}