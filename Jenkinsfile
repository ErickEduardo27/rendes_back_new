@Library(['git_essalud_lib','common_essalud_lib','docker_essalud_lib','nodejs_essalud_lib']) _

def gitLib = new git_essalud_lib()
def commonLib = new common_essalud_lib()
def dockerLib = new docker_essalud_lib()
def nodejsLib = new nodejs_essalud_lib()

pipeline {

    agent any

    tools {
        'org.jenkinsci.plugins.docker.commons.tools.DockerTool' 'docker-tool'
        nodejs 'nodejs-tool-16'
    }

    environment {
        GROUP_ID = '53f1e202-16de-4656-8210-fd428afb9a2f'
        APPLICATION_ID = 'c0d842d8-1a38-48a8-b98c-6fe88e96ac25'
    }

    options {
        skipStagesAfterUnstable()
        disableConcurrentBuilds abortPrevious: true
        buildDiscarder(logRotator(numToKeepStr: "${JOB_MAX_DAYS}", daysToKeepStr: "${JOB_MAX_BUILDS}"))
    }

    stages {
    
        stage('Check Tools') {
            steps {
                script {
                    commonLib.msgJobBuildStarted()
                    nodejsLib.showToolVersion()
                    dockerLib.showToolVersion()
                 }
            }
        }

        stage('Clone Repository') {
            steps {
                checkout scm

                script {
                    gitLib.cloneEnv()
                    commonLib.showWsFiles()
                }
            }
        }

        stage('Build Image') {
            steps {
                script { 
                    dir("codigo/back") {
                        commonLib.showWsFiles()
                        dockerLib.buildImage() 
                    }
                }
            }
        }

        stage('Push Image') {
            steps {
                script { dockerLib.pushImage() }
            }
        }

        stage('Deploy') {
            steps {
                script { dockerLib.runContainer() }
            }
        }

    }

    post {
        always { cleanWs() }
        success { script { commonLib.msgJobBuildSuccess() } }
        failure { script { commonLib.msgJobBuildFailed() } }
        unstable { script { commonLib.msgJobBuildUnstable() } }
    }

}
