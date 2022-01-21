# -*- coding: utf-8 -*-

"""
Mastermind classes
"""

import json
import pygame

# Couleurs
couleur = {
    "black": pygame.Color(0, 0, 0),
    "white": pygame.Color(255, 255, 255),
    "red": pygame.Color(255, 0, 0),
    "green": pygame.Color(0, 255, 0),
    "blue": pygame.Color(0, 0, 255),
    "yellow": pygame.Color(255, 255, 0),
    "darkgray": pygame.Color(169, 169, 169),
    "cyan": pygame.Color(0, 255, 255),
    "brown": pygame.Color(153, 85, 51),
    "dark_brown": pygame.Color(90, 54, 20),
    "gold": pygame.Color(255, 200, 0)
}
couleur_mastermind_ID = {
    1: "red",
    2: "blue",
    3: "green",
    4: "yellow",
    5: "white",
    6: "black"
}


def charger_ressource(path):
    """
    Permet de lire les ressources du jeu.

    >>> charger_ressource("/sprites/info.png")
    """
    ressource = pygame.image.load(f"./ressources{path}")
    return ressource


class Spritesheet:
    """
    Objet s'occupant d'un fichier type spritesheet.
    """
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data, encoding="utf-8") as fichier:
            self.data = json.load(fichier)
        fichier.close()

    def get_sprite(self, x_position, y_position, width, heigth):
        """
        Permet d'avoir le sprite avec sa position x, sa position y,
        sa taille et sa hauteur.
        """
        sprite = pygame.Surface((width, heigth))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(
            self.sprite_sheet,
            (0, 0),
            (x_position, y_position, width, heigth)
        )
        return sprite

    def parse_sprite(self, name):
        """
        Permet de dessiner le sprite.
        """
        sprite = self.data['frames'][name]['frame']
        x_position, y_position = sprite["x"], sprite["y"]
        w_position, h_position = sprite["w"], sprite["h"]
        image = self.get_sprite(x_position, y_position, w_position, h_position)
        return image


class Button:
    """
    Objet s'occupant d'un bouton.
    """
    def __init__(self, sprite, rect):
        self._sprite = sprite
        self._x = rect[0]
        self._y = rect[1]
        self._width = rect[2]
        self._heigth = rect[3]
        self._rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])

    def draw(self, screen):
        """
        Permet de dessiner le bouton sur une surface.
        """
        rect_value = (self._width, self._heigth)
        sprite = pygame.transform.scale(self._sprite, rect_value)
        screen.blit(sprite, (self._x, self._y))

    def event_handler(self, event):
        """
        Permet de détecter si le joueur a fait un clique gauche
        sur le bouton.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self._rect.collidepoint(event.pos):
                    return True
        return False


class Parallax:
    """
    Objet s'occupant de l'animation d'un fond d'écran.
    """
    def __init__(self, sprite, speed, flip=False):
        self._sprite = sprite
        self._speed = speed
        self._bgs_width_position = [0, 1280]
        background = charger_ressource(f"/sprites/{sprite}")
        if flip is not False:
            self._background1 = pygame.transform.scale(background, (1280, 720))
            flipped_bg = pygame.transform.scale(background, (1280, 720))
            self._background2 = pygame.transform.flip(flipped_bg, True, False)
        else:
            self._background1 = pygame.transform.scale(background, (1280, 720))
            self._background2 = pygame.transform.scale(background, (1280, 720))

    def draw(self, screen):
        """
        Permet de dessiner le fond d'écran sur la surface.
        """
        self._bgs_width_position[0] -= self._speed
        self._bgs_width_position[1] -= self._speed

        if self._bgs_width_position[0] <= -1280:
            self._bgs_width_position[0] = 1280
        elif self._bgs_width_position[1] <= -1280:
            self._bgs_width_position[1] = 1280

        screen.blit(self._background1, (self._bgs_width_position[0], 0))
        screen.blit(self._background2, (self._bgs_width_position[1], 0))


class Grille:
    """
    Objet s'occupant de la grille.
    """
    def __init__(self, xdef, ydef, var):
        self._xdef = xdef
        self._ydef = ydef
        self._table = [
            [
                0 for i in range(var["nb_couleurs"])
            ]
            for j in range(var["essaies"])
        ]
        self._checker = [
            [
                "X" for i in range(2)
            ]
            for j in range(var["essaies"])
        ]
        self._limx, self._limy = 375, 600
        self._blocktaille, self._rects, self._rects_background = 100000, [], []

        # Déduction de la taille d'une seule case
        while True:
            x_position = self._xdef * self._blocktaille
            y_position = self._ydef * self._blocktaille
            if x_position > self._limx or y_position > self._limy:
                self._blocktaille -= 1
                continue
            break

        # Remplissage de rects
        debut_x = (self._limx - self._blocktaille * xdef) / 2
        debut_y = (self._limy - self._blocktaille * ydef) / 2
        for x1_position in range(0, y_position, self._blocktaille):
            rect_selected = []
            rect_background = []
            for y1_position in range(0, x_position, self._blocktaille):
                rect = pygame.Rect(
                    y1_position+debut_y+50,
                    x1_position+debut_x,
                    self._blocktaille - 5,
                    self._blocktaille - 5
                )
                rect_cote = pygame.Rect(
                    (y1_position+debut_y+50) - 3,
                    (x1_position+debut_x) - 3,
                    self._blocktaille + 2,
                    self._blocktaille + 2
                )
                rect_selected.append(rect)
                rect_background.append(rect_cote)
            self._rects.append(rect_selected)
            self._rects_background.append(rect_background)

    def draw(self, screen, var):
        """
        Permet de dessiner la grille sur une surface.
        """
        # placement des cases du jeu
        for i in enumerate(self._table):
            for k in enumerate(self._table[i[0]]):
                pygame.draw.rect(
                    screen,
                    couleur["dark_brown"],
                    self._rects_background[i[0]][k[0]]
                )
                if self._table[i[0]][k[0]] == 0:
                    pygame.draw.rect(
                        screen,
                        couleur["brown"],
                        self._rects[i[0]][k[0]]
                    )
                else:
                    pygame.draw.rect(
                        screen,
                        couleur[self._table[i[0]][k[0]]],
                        self._rects[i[0]][k[0]]
                    )
        # Placement des valeurs du checker
        x_space = self._rects[0][-1].width
        x_position = self._rects[0][-1].x + x_space + 20
        y_position = self._rects[0][-1].y
        for i in enumerate(self._checker):
            for k in enumerate(self._checker[i[0]]):
                if self._checker[i[0]][k[0]] != "X":
                    valuechecker = var["fonts"]["determination_font"].render(
                        f"{self._checker[i[0]][k[0]]}",
                        1,
                        couleur["gold"]
                    )
                    screen.blit(valuechecker, (x_position, y_position))
                x_position += x_space
            x_position = self._rects[0][-1].x + x_space + 20
            y_position = y_position + (
                self._rects[1][-1].y - self._rects[0][-1].y
            )

        # Placement des deux logos pour signifier les information du checker
        screen.blit(
            pygame.transform.scale(
                charger_ressource("/sprites/checkmark.png"),
                (35, 35)
            ),
            (x_position - 5, y_position + 5)
        )
        screen.blit(
            pygame.transform.scale(
                charger_ressource("/sprites/info.png"),
                (35, 35)
            ),
            ((x_position + x_space) - 5, y_position + 5)
        )

    def put_colors(self, data):
        """
        Permet de pouvoir mettre une couleur sur une case de la
        grille.
        """
        for i in enumerate(self._table):
            for k in enumerate(self._table[i[0]]):
                if self._table[i[0]][k[0]] == 0:
                    self._table[i[0]] = data
                    return

    def put_checker(self, data):
        """
        Permet de pouvoir mettre une valeur dans le checker.
        """
        for i in enumerate(self._checker):
            for k in enumerate(self._checker[i[0]]):
                if self._checker[i[0]][k[0]] == "X":
                    self._checker[i[0]] = data
                    return


class Selection:
    """
    Objet s'occupant de la sélection.
    """
    def __init__(self, var):
        self._nb_couleurs = var["nb_couleurs"]
        self._colors = []
        self._grille = var["grille"]
        couleurs_id_liste = list(couleur_mastermind_ID.values())
        self._couleurs = couleurs_id_liste[:var["nb_couleurs"]]

        self._selection, self._buttons_haut = [], []
        self._buttons_bas, self._validation_liste = [], {
            "OK": 0,
            "POSITION_ISSUE": 0
        }
        self._button_const_position = (759, 430)
        x_position, y_position = self._button_const_position
        xcons = x_position
        while x_position <= xcons + (60 * self._nb_couleurs-1):
            self._selection.append(self._couleurs)
            self._buttons_haut.append(
                Button(
                    charger_ressource("./sprites/haut.png"),
                    [x_position, y_position, 50, 50]
                )
            )
            x_position += 60
        x_position -= (60 * self._nb_couleurs)
        y_position += 120
        xcons = x_position
        while x_position <= xcons + (60 * self._nb_couleurs-1):
            self._buttons_bas.append(
                Button(
                    charger_ressource("./sprites/bas.png"),
                    [x_position, y_position, 50, 50]
                )
            )
            x_position += 60

        self._surface = pygame.Surface((63 * len(self._buttons_haut), 265))
        self._surface.fill(couleur["dark_brown"])
        self._surface_temp = pygame.Surface(
            (60 * len(self._buttons_haut), 255)
            )
        self._surface_temp.fill(couleur["brown"])
        self._surface.blit(self._surface_temp, (5, 5))

        self._surface_validation = pygame.Surface(
            (
                245,
                160
            )
        )
        self._surface_validation.fill(couleur["dark_brown"])
        surface_temp_validation = pygame.Surface(
            (
                250,
                150
            )
        )
        surface_temp_validation.fill(couleur["brown"])
        self._surface_validation.blit(surface_temp_validation, (5, 5))
        self._surface_validation.blit(
            pygame.transform.scale(
                charger_ressource("/sprites/checker.png"),
                (236, 57)
            ),
            (4, 15)
        )

        self._checker_const_position = (12, 80)
        x_position, y_position = self._checker_const_position

        self._surface_validation.blit(
            pygame.transform.scale(
                charger_ressource("/sprites/checkmark.png"),
                (45, 45)
            ),
            (x_position+10, y_position)
        )

        self._surface_validation.blit(
            pygame.transform.scale(
                charger_ressource("/sprites/info.png"),
                (45, 45)
            ),
            (x_position+115, y_position)
        )

        self._valider = Button(
            charger_ressource("./sprites/valider.png"),
            [
                60 * len(self._buttons_haut) + 610,
                615,
                140,
                50
            ]
        )

        self._rejouer = Button(
            charger_ressource("./sprites/rejouer.png"),
            [
                60 * len(self._buttons_haut) + 610,
                615,
                140,
                50,
            ]
        )

    def draw_buttons(self, screen):
        """
        Permet de dessiner les boutons de sélection des couleurs
        sur une surface.
        """
        x_position, y_position = self._button_const_position
        for i in range(self._nb_couleurs):
            self._buttons_haut[i].draw(screen)
            self._buttons_bas[i].draw(screen)
            pygame.draw.rect(
                screen,
                couleur[self._selection[i][0]],
                (x_position + 2, y_position + 60, 45, 45)
            )
            x_position += 60
        self._valider.draw(screen)

    def draw_win(self, screen, var):
        """
        Permet de dessiner la surface pour dire que l'utilisateur a gagné.
        """
        wintext = var["fonts"]["littleshort_determination_font"].render(
            "Félicitations !",
            1,
            couleur["gold"]
        )
        text_rect = wintext.get_rect(center=self._surface.get_rect().center)
        self._surface.blit(wintext, (text_rect.x, text_rect.y))
        self._rejouer.draw(screen)

    def draw_checker(self, var):
        """
        Permet de dessiner la vérification du checker des couleurs
        sur la surface.
        """
        position_issue_count = self._validation_liste["POSITION_ISSUE"]
        ok_count = self._validation_liste["OK"]
        pygame.draw.rect(
            self._surface_validation,
            couleur["brown"],
            pygame.Rect(83, 72, 30, 50)
        )
        pygame.draw.rect(
            self._surface_validation,
            couleur["brown"],
            pygame.Rect(189, 72, 30, 50)
        )
        ok_text = var["fonts"]["determination_font"].render(
            str(ok_count),
            1,
            couleur["gold"]
        )
        position_issue_text = var["fonts"]["determination_font"].render(
            str(position_issue_count),
            1,
            couleur["gold"]
        )
        self._surface_validation.blit(ok_text, (85, 72))
        self._surface_validation.blit(position_issue_text, (190, 72))

    def draw(self, screen):
        """
        Permet de dessiner les outils sur une surface.
        """
        screen.blit(self._surface, (750, 420))
        screen.blit(self._surface_validation, (510, 110))

    def change_couleur_haut(self, index):
        """
        Permet de changer la couleur d'une sélection précise
        de droite à gauche.
        """
        test = self._selection[index].copy()
        test.append(test.pop(0))
        self._selection[index] = test

    def change_couleur_bas(self, index):
        """
        Permet de changer la couleur d'une sélection précise
        de gauche à droite.
        """
        test = self._selection[index].copy()
        value = test.pop(-1)
        test.insert(0, value)
        self._selection[index] = test

    def valider(self, grille):
        """
        Permet de traiter la sélection quand le joueur aura cliqué
        sur le bouton "Valider".
        """
        self._colors = []
        for i in enumerate(self._selection):
            self._colors.append(self._selection[i[0]][0])
        grille.put_colors(self._colors)

    def check_validation(self, code):
        """
        Permet de regarder et de traiter les réponses de la
        sélection avec le code généré.
        """
        validation_templist = {"OK": 0, "POSITION_ISSUE": 0}
        test_code = code.copy()
        position_issue_liste = []
        for i in enumerate(self._colors):
            if self._colors[i[0]] == test_code[i[0]]:
                validation_templist["OK"] += 1
            else:
                position_issue_liste.append(i[0])
        for i in enumerate(position_issue_liste):
            wrong_place = False
            for j in enumerate(position_issue_liste):
                if self._colors[i[1]] == test_code[j[1]]:
                    wrong_place = True
            if wrong_place:
                validation_templist["POSITION_ISSUE"] += 1
        self._validation_liste = validation_templist
        self._grille.put_checker(
            [
                self._validation_liste["OK"],
                self._validation_liste["POSITION_ISSUE"]
            ]
        )

    def change_selection(self, color):
        """
        Permet de changer la sélection de couleur.
        """
        index = 0
        while index != self._nb_couleurs:
            for i in range(self._nb_couleurs):
                if self._selection[index][0] == color[index]:
                    index += 1
                    break
                else:
                    self.change_couleur_haut(index)
