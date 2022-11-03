pipeline {
    agent any
  
	environment{
		FLASK_APP='autoapp.py'
		FLASK_DEBUG=1
		FLASK_ENV='development'
		DATABASE_URL='sqlite:///dev.db'
		GUNICORN_WORKERS=1
		LOG_LEVEL='debug'
		SEND_FILE_MAX_AGE_DEFAULT=0

		SECRET_KEY = credentials('SECRET_KEY')
		SECURITY_PASSWORD_SALT = credentials('SECURITY_PASSWORD_SALT')
		JWT_KEY = credentials('JWT_KEY')

		RECAPTCHA_SITE_KEY = credentials('RECAPTCHA_SITE_KEY')
		RECAPTCHA_SECRET_KEY = credentials('RECAPTCHA_SECRET_KEY')
		RECAPTCHA_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'

		MAIL_DEFAULT_SENDER = credentials('MAIL_DEFAULT_SENDER')
		MAIL_PASSWORD = credentials('MAIL_PASSWORD')
		DOCKERHUB_CREDENTIALS=credentials('DOCKER_HUB_CREDS')
	}

    stages {
        stage('Build') {
            steps {
                echo '========== BUILDING OPENCERT =========='
				sh 'apk update'
				sh 'apk add build-base'
				sh 'apk add npm'
				sh 'pip3 install --no-cache --upgrade pip setuptools'
				sh 'pip3 install -r ./requirements/prod.txt'
				sh 'flask db init || true'
				sh 'flask db migrate'
				sh 'flask db upgrade'
				sh 'npm install'
				sh 'npm run-script build'
				sh 'touch .env'
				sh 'echo FLASK_APP=autoapp.py >> .env'
				echo '========== BUILDING SUCCESFUL =========='
			}	
        }
        // stage('Automated Testing') {
        //     steps {
        //         echo '========== TESTING OPENCERT =========='
        //         sh 'flask test || true'
        //         echo '========== TESTING COMPLETED =========='
        //     }
        // }
		// stage('OWASP DependencyCheck'){
		// 	steps {
		// 	echo '========== PERFORMING OWASP DEPENDENCY CHECK =========='
		// 	dependencyCheck additionalArguments: '--noupdate --disableAssembly --format HTML --format XML --disableYarnAudit --exclude ./opencert', odcInstallation: 'Default'
		// 	echo '========== OWASP DEPENDENCY CHECK SUCCESSFUL =========='
		// 	}
		// }
		// stage('SonarQube Quality Check'){
		// 	steps {
		// 		echo '========== PERFORMING SONARQUBE SCAN =========='
		// 		script {
		// 			def scannerHome = tool 'SonarQube';
		// 			withSonarQubeEnv('SonarQube') {
		// 			sh "${scannerHome}/bin/sonar-scanner -Dsonar.javascript.node.maxspace=2560 -Dsonar.projectKey=OPENCERT -Dsonar.sources=./opencert"
		// 			}
		// 		}
		// 		echo '========== SONARQUBE SCAN SUCCESSFUL =========='
		// 	}
		// }
		stage('Build Docker Image'){
			steps{
				sh 'docker compose build flask-prod'
			}
		}
		stage('Login to DockerHub'){
			steps{
				sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
			}
		}
		stage('Deploy to DockerHub'){
			steps{
				sh 'docker push 3x03t18/opencert'
			}
		}
    }
  post {
    success {
      dependencyCheckPublisher pattern: 'dependency-check-report.xml'
    }
    always {
      recordIssues enabledForFailure: true, tool: sonarQube()
    }
  }
}