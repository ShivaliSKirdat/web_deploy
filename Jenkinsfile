pipeline {
   agent any
  
   environment {
       DOCKER_HUB_REPO = "shivalikirdat/web_deploy"
       CONTAINER_NAME = "web_deploy" 
   }
  
   stages {
       stage('Checkout') {
           steps {
               //checkout([$class: 'GitSCM', credentialsId: '1e2767da-313f-47ba-8a90-66205de0cea8', branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/ShivaliSKirdat/web_deploy']]])
                 git branch: 'main', credentialsId: '1e2767da-313f-47ba-8a90-66205de0cea8', url: 'https://github.com/ShivaliSKirdat/web_deploy.git'
           }
       }
       stage('Build') {
           steps {
               echo 'Building..'
               sh 'docker image build -t $DOCKER_HUB_REPO:latest .'
           }
       }
       stage('SonarQube Analysis') {
          steps {
            script {
               def scannerHome = tool 'SonarQube' // Assuming you have configured SonarQube Scanner as a tool in Jenkins
               //def scannerHome = tool 'SonarQube Scanner for Jenkins'
               withSonarQubeEnv('SonarQube Server') {
               sh "${scannerHome}/bin/sonar-scanner"
               }
            }
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

post {
    always {
      // Publish the SonarQube results as a post-build action
      sonarQubeScan()
    }
  }
