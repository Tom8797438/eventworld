

:: **Démarrage du serveur Django**
cd D:\Projets\Eventworld\eventworld
echo 🚀 Démarrage du serveur backend...
start /b python manage.py runserver

:: **Démarrage du serveur frontend**
cd D:\Projets\Eventworld\eventworld\frontend\frontendEventWorld
echo 🚀 Démarrage du serveur frontend...
start /b npm run dev

:: Retour à la racine
cd D:\Projets\Eventworld\eventworld
echo ✅ Les serveurs backend et frontend sont activés.

pause
