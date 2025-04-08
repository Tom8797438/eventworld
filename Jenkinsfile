pipeline {
    agent any

    environment {
        BACKEND_DIR = "EventWorldApp/EventWorldApp"
        FRONTEND_DIR = "Eventworld/frontend/frontendEventWorld"
    }

    stages {
        stage('Cloner le projet') {
            steps {
                git branch: 'main', url: 'https://gitlab.com/Tom8797438/eventworld.git'
            }
        }

        stage('Lancer le backend') {
            steps {
                echo "📥 Clonage du dépôt backend GitLab"
                sh '''
                    cd $BACKEND_DIR
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                    python manage.py migrate
                    nohup python manage.py runserver 0.0.0.0:8000 &
                '''
            }
        }

        stage('Lancer le frontend') {
            steps {
                echo "📥 Clonage du dépôt frontend GitLab"
                sh '''
                    cd $FRONTEND_DIR
                    npm install
                    nohup npm run dev > frontend.log 2>&1 &
                '''
            }
        }
    }
}
