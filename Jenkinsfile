pipeline {
    agent any
    parameters {
        string(name: 'STUDENT_NAME', defaultValue: 'Иванов Иван', description: 'ФИО студента')
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'production'], description: 'Cреда')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Запускать тесты')
    }
    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_IMAGE = "cxzyueiifqqe/student-app:${BUILD_NUMBER}"
        CONTAINER_NAME = "student-app-${ENVIRONMENT}"
    }
    stages {
        stage('Checkout') {
            steps {
                echo 'Клонирование репозитория...'
                git branch: 'main', credentialsId: 'github-credentials', url: 'https://github.com/2dollar2dollar/simple-python-app.git'
            }
        }
        stage('Tests') {
            when { expression { params.RUN_TESTS } }
            steps {
                echo 'Запуск тестов...'
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                python -m unittest test_app.py -v
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                echo 'Сборка Docker образа...'
                script {
                    docker.build("${DOCKER_IMAGE}")
                }
            }
        }
        stage('Push to Registry') {
            steps {
                echo 'Публикация образа в Docker Hub...'
                script {
                    docker.withRegistry('', 'docker-hub-credentials') {
                        docker.image("${DOCKER_IMAGE}").push()
                    }
                }
            }
        }
        stage('Deploy to Dev') {
            when { expression { params.ENVIRONMENT == 'dev' } }
            steps {
                echo 'Развертывание в DEV...'
                sh "docker rm -f ${CONTAINER_NAME} || true"
                sh "docker run -d --name ${CONTAINER_NAME} -p 8081:5000 -e STUDENT_NAME='${params.STUDENT_NAME}' ${DOCKER_IMAGE}"
            }
        }
        stage('Deploy to Staging') {
            when { expression { params.ENVIRONMENT == 'staging' } }
            steps {
                echo 'Развертывание в STAGING...'
                sh "docker rm -f ${CONTAINER_NAME} || true"
                sh "docker run -d --name ${CONTAINER_NAME} -p 8082:5000 -e STUDENT_NAME='${params.STUDENT_NAME}' ${DOCKER_IMAGE}"
            }
        }
        stage('Approve Production') {
            when { expression { params.ENVIRONMENT == 'production' } }
            steps {
                input message: "Подтвердите развертывание в PRODUCTION?", ok: "Да, развернуть"
            }
        }
        stage('Deploy to Production') {
            when { expression { params.ENVIRONMENT == 'production'} }
            steps {
                echo "Развертывание в PRODUCTION одобрено"
                sh "docker rm -f ${CONTAINER_NAME} || true"
                sh "docker run -d --name ${CONTAINER_NAME} -p 80:5000 -e STUDENT_NAME='${params.STUDENT_NAME}' ${DOCKER_IMAGE}"
            }
        }
    }
    post {
        always {
            echo 'Очистка рабочего пространства...'
            cleanWs()
        }
        success {
            echo "Pipeline успешно выполнен для ${params.ENVIRONMENT}"
        }
        failure {
            echo "Pipeline failed: ${env.JOB_NAME}. Проверьте логи."
        }
    }
}
