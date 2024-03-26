import os
import threading
import time


class GetCoordonate(threading.Thread):
    def __init__(self, fichier,  main_window, running=False):
        super().__init__()
        self.fichier = fichier
        self.taille_actuelle = 0
        self.main_window = main_window
        self.running = running
        self.finished = False

    def run(self):
        count = 0
        obstacle_mode = False
        while not self.finished:
            while self.running:
                taille_nouvelle = os.path.getsize(self.fichier)
                if taille_nouvelle > self.taille_actuelle:
                    with open(self.fichier, 'r') as f:
                        lignes = f.readlines()
                        nouvelle_ligne = lignes[-1].strip()
                        nouvelle_ligne = nouvelle_ligne[10:]
                        print(nouvelle_ligne)
                        if "----" in nouvelle_ligne:
                            obstacle_mode = not obstacle_mode
                            if obstacle_mode == False:
                                self.main_window.map.index_figure += 1
                            print("Mode obstacle : {}".format(obstacle_mode))
                        else:
                            nouvelle_ligne = nouvelle_ligne[:-1]
                            nouvelle_ligne = nouvelle_ligne.split("(")[1]
                            x, z, y = nouvelle_ligne.split(", ")
                            if count != 0:
                                self.main_window.add_point(float(x), float(y))
                        # self.main_window.update_plot()
                    self.taille_actuelle = taille_nouvelle
                count += 1
                time.sleep(0.2)  # Attendre un certain temps avant de vérifier à nouveau
            time.sleep(0.2)
    def stop(self):
        self.running = False
        self.finished = True