pipeline{
	agent any 
	stages{
		stage('Git Checkout'){
			steps{
				echo 'Checkout stage'
			}
		}
		
		stage('Build image'){
			steps {
                echo 'Starting to build docker image'

            }
		}
		
		stage('Lint') {
            steps {
                echo 'Linting..'
                
            }
        }
		
		stage('Test') {
            steps {
                echo 'Testing ..'
                
            }
        }
				
		stage('Deploy') { 
			steps { 
				echo 'Deploy stage'
				
			} 
		} 
	}
}