pipeline {
   agent any
  
   environment {
       DOCKER_HUB_REPO = "shivalikirdat/web_deploy"
       CONTAINER_NAME = "web_deploy" 
   }
  
   stages {
       stage('Checkout') {
           steps {
               checkout([$class: 'GitSCM', branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/ShivaliSKirdat/web_deploy']]])
           }
       }
       stage('Build') {
           steps {
               echo 'Building..'
               sh 'docker image build -t $DOCKER_HUB_REPO:latest .'
           }
       }
    //    stage('Test') {
    //        steps {
    //            echo 'Testing..'
    //            sh 'docker stop $CONTAINER_NAME || true'
    //            sh 'docker rm $CONTAINER_NAME || true'
    //            sh 'docker run --name $CONTAINER_NAME $DOCKER_HUB_REPO /bin/bash -c "pytest test.py && flake8"'
    //        }
    //    }
       stage('Deploy') {
           steps {
               echo 'Deploying....'
               sh 'docker stop $CONTAINER_NAME || true'
               sh 'docker rm $CONTAINER_NAME || true'
               sh 'docker run -d -p 5000:5000 --name $CONTAINER_NAME $DOCKER_HUB_REPO'
           }
       }
   }
}
