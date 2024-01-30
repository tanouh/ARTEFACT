import pygame
from pygame.locals import *

def use_joystick():
    pygame.init()
    pygame.joystick.init()

    # verify that at least one joystick is connected
    if pygame.joystick.get_count() == 0:
        print("Aucun joystick détecté.")
        pygame.quit()
        quit()

    # init first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("!!!! Detected joystick  :", joystick.get_name())
    for event in pygame.event.get():
        if event.type == QUIT:
            pass
        elif event.type == JOYAXISMOTION:
        #     Mouvement suivant l'axe Y
            if event.axis == 1:
                # Seuil pour considérer le mouvement vers l'avant
                if event.value < -0.5:
                    print("Avancer")
                # Seuil pour considérer le mouvement vers l'arrière
                elif event.value > 0.5:
                    print("Reculer")
                else:
                    print("Arrêt")
            else:
                # Mouvement suivant l'axe X
                # Seuil pour considérer le mouvement vers la droite
                if event.value > 0.5:
                    print("Joystick incliné vers la droite")
                # Seuil pour considérer le mouvement vers la gauche
                elif event.value < -0.5:
                    print("Joystick incliné vers la gauche")
        elif event.type == JOYBUTTONDOWN:
            print("Bouton {} pressé".format(event.button))



if __name__ == '__main__':
        use_joystick()