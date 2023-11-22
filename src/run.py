from camera  import stream_cam as s
from camera import realtime_detection as rd
from motor.app import app
from threading import Thread as th

if __name__ == '__main__':
        # Créez deux threads, un pour le serveur Flask et un pour la détection d'image
        flask_thread = th(target=app.launch_site)
        detection_thread = th(target=s.launch_streaming)

        # Lancez les deux threads
        flask_thread.start()
        detection_thread.start()
        
        # Attendez que les deux threads se terminent (ce qui ne se produira pas dans cet exemple)
        flask_thread.join()
        detection_thread.join()


