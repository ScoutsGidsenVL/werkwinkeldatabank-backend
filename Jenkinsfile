pipeline {
  agent any

  options {
    buildDiscarder(logRotator(artifactNumToKeepStr: '10'))
  }

  stages {
    stage('deploy') {
      steps {
        sh 'ssh ad-deb-mgmt sudo -u ansible /opt/deploy-wwdb.sh backend ${BRANCH_NAME}'
      }
    }
  }

  post {
    failure {
      emailen()
    }
    unstable {
      emailen()
    }
    changed {
      emailen()
    }
  }
}

def emailen() {
  mail(
    to: "tvl@scoutsengidsenvlaanderen.be,boro@inuits.eu,ricardo@inuits.eu,${env.CHANGE_AUTHOR_EMAIL}",
    subject: "[Jenkins] ${currentBuild.fullDisplayName} ${currentBuild.currentResult}",
    body: """${currentBuild.fullDisplayName} ${currentBuild.currentResult}

${currentBuild.absoluteUrl}"""
  )
}
