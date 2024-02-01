# Projet ARTEFACT 2024
Développé par l'équipe 8B composé de : 
- Tania Mahandry
- Zhiying Zou
- Alexandre Mallez

## Architecture du projet
Le code source est répartie sous plusieurs modules : 
- Module de la caméra : 
    - **realtime_detection.py** : 
        - `class Detector()`: englobe les fonctions de détection des marqueurs aruco, et la conduite autonome. 
    - **stream_cam.py**: 
        - `class Streamer()` : responsable de la connexion avec le port de la caméra et de la lecture des images capturées par celle-ci 

- Module du moteur : 
    - Templates : 
        - **ui.html**: code source de l'interface web
    - **PCA9685.py** : script pour l'alimentation des moteurs, directement tiré de : [source](https://www.waveshare.com/wiki/Motor_Driver_HAT)
    - **motor_controller.py** : bibliothèques de fonctions liées aux mouvements du robot
    - **motor_driver.py**: 
        - `class MotorDriver()`: module pour piloter les moteurs 
    - **mylib.py**: bibliothèques de fonctions utiles pour le serveur
    - **app.py**: implémentation du serveur 

## Choix technologiques:

Certains choix des technologies utilisées sont complètement arbitraires tandis que d'autres ont été suggérés. 

Les bibliothèques externes de python utilisées : 
- ***OpenCV*** : pour la gestion de la caméra et la détection des aruco
- ***Flask*** : pour le serveur web
- ***smbus*** : pour la communication entre la carte RPI et le Motor Driver

 
