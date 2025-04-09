pipeline {
    agent any

    stage('Lister les fichiers') {
            steps {
                sh 'pwd'
                sh 'ls -la'
                sh 'ls -R'
            }
        }

    stages {
        stage('Déploiement avec Docker Compose') {
            steps {
                 sh 'docker-compose -f Eventworld/eventworld/docker-compose.yml up -d --build'
            }
        }
    }
}


// pipeline {
//     agent any

//     environment {
//             BACKEND_DIR = "EventWorldApp"
//             FRONTEND_DIR = "frontend/frontendEventWorld"
//             }


//     stages {
//         stage('Cloner le projet') {
//             steps {
//                 git branch: 'main', url: 'https://gitlab.com/Tom8797438/eventworld.git'
//             }
//         }

//     // stage('Lister les fichiers') {
//     //     steps {
//     //         sh 'pwd'
//     //         sh 'ls -la'
//     //         sh 'ls -R'
//     //     }
//     // }

//         stage('Lancer le backend') {
//             steps {
//                 echo "📥 Clonage du dépôt backend GitLab"
//                 sh "echo BACKEND_DIR=$BACKEND_DIR"
//                 sh '''
//                     cd $BACKEND_DIR
//                     pip install -r requirements.txt
//                     python manage.py migrate
//                     nohup python manage.py runserver 0.0.0.0:8000 &
//                 '''
//             }
//         }

//         stage('Lancer le frontend') {
//             steps {
//                 echo "📥 Clonage du dépôt frontend GitLab"
//                 sh "echo BACKEND_DIR=$FRONTEND_DIR"

//                 sh '''
//                     cd $FRONTEND_DIR
//                     npm install
//                     nohup npm run dev > frontend.log 2>&1 &
//                 '''
//             }
//         }
//     }
// }

