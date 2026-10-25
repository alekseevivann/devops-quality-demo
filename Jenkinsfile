pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
        disableConcurrentBuilds()
    }

    environment {
        IMAGE = "registry.example.com/demo/app:${env.GIT_COMMIT}"
        PIP_CACHE_DIR = "${env.WORKSPACE}/.cache/pip"
    }

    stages {
        stage('Подготовка окружения') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt -r requirements-dev.txt
                '''
            }
        }

        stage('Линтер') {
            steps {
                sh '. .venv/bin/activate && flake8 app tests'
            }
        }

        stage('Модульные тесты') {
            steps {
                sh '''
                    . .venv/bin/activate
                    mkdir -p reports
                    pytest --junitxml=reports/junit.xml \
                           --cov=app --cov-report=xml:reports/coverage.xml \
                           --cov-fail-under=80
                '''
            }
            post {
                always {
                    junit 'reports/junit.xml'
                }
            }
        }

        stage('SAST (Bandit)') {
            steps {
                sh '. .venv/bin/activate && bandit -r app -ll -f json -o reports/bandit.json'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/*.json, reports/*.xml',
                                     allowEmptyArchive: true
                }
            }
        }

        stage('Сборка образа') {
            steps {
                sh 'docker build -t $IMAGE .'
            }
        }

        stage('Выкладка в staging') {
            when { branch 'main' }
            steps {
                sh './deploy.sh staging $IMAGE'
            }
        }

        stage('Подтверждение выкладки') {
            when { branch 'main' }
            steps {
                timeout(time: 1, unit: 'DAYS') {
                    input message: 'Выкатить в production?', ok: 'Выкатить'
                }
            }
        }

        stage('Выкладка в production') {
            when { branch 'main' }
            steps {
                sh './deploy.sh production $IMAGE'
            }
        }
    }

    post {
        failure {
            echo 'Конвейер завершился с ошибкой: проверьте отчёты и журнал сборки.'
        }
        cleanup {
            cleanWs()
        }
    }
}
