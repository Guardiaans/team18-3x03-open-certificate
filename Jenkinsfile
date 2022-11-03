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
				sh 'docker compose build flask-prod --build-arg FLASK_APP=${FLASK_APP} \
													--build-arg FLASK_DEBUG=${FLASK_DEBUG} \
													--build-arg FLASK_ENV=${FLASK_ENV} \
													--build-arg DATABASE_URL=${DATABASE_URL} \
													--build-arg GUNICORN_WORKERS=${GUNICORN_WORKERS} \
													--build-arg LOG_LEVEL=${LOG_LEVEL} \
													--build-arg SEND_FILE_MAX_AGE_DEFAULT=${SEND_FILE_MAX_AGE_DEFAULT} \
													--build-arg SECRET_KEY=${SECRET_KEY} \
													--build-arg SECURITY_PASSWORD_SALT=${SECURITY_PASSWORD_SALT} \
													--build-arg JWT_KEY=${JWT_KEY} \
													--build-arg RECAPTCHA_SITE_KEY=${RECAPTCHA_SITE_KEY} \
													--build-arg RECAPTCHA_SECRET_KEY=${RECAPTCHA_SECRET_KEY} \
													--build-arg RECAPTCHA_VERIFY_URL=${RECAPTCHA_VERIFY_URL} \
													--build-arg MAIL_DEFAULT_SENDER=${MAIL_DEFAULT_SENDER} \
													--build-arg MAIL_PASSWORD=${MAIL_PASSWORD}'
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