# -*- coding: utf-8 -*-

"""
MASTERMIND

Jeu crée et programmé par Jouca / Diego pour le projet de NSI 1er Trimestre.
Ce jeu reprend les bases du mastermind sur un nouveau design fait pour
les joueurs avec une génération aléatoire de code par le programme!
"""

import random
import pygame
from itertools import product
from ressources.classes import Spritesheet, Button, Grille, Parallax
from ressources.classes import Selection, charger_ressource

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
# Indentifiants des couleurs
couleur_mastermind_ID = {
    1: "red",
    2: "blue",
    3: "green",
    4: "yellow",
    5: "white",
    6: "black"
}

screen_size = (1280, 720)


def init_screen():
    """
    Initialise les paramètres de pygame.
    """
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.mixer.music.set_volume(0.7)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Mastermind")
    pygame.display.set_icon(charger_ressource("/sprites/mastermind_logo.png"))
    return screen


def init_fonts():
    """
    Initialise les polices d'écritures.
    """
    fonts = {
        "big_generalfont": pygame.font.Font(
            "./ressources/polices/PetMe64.ttf",
            60
        ),
        "normal_generalfont": pygame.font.Font(
            "./ressources/polices/PetMe64.ttf",
            40
        ),
        "littlenormal_generalfont": pygame.font.Font(
            "./ressources/polices/PetMe64.ttf",
            35
        ),
        "big_pusab": pygame.font.Font(
            "./ressources/polices/Pusab.ttf",
            60
        ),
        "normal_pusab": pygame.font.Font(
            "./ressources/polices/Pusab.ttf",
            40
        ),
        "littlenormal_pusab": pygame.font.Font(
            "./ressources/polices/Pusab.ttf",
            30
        ),
        "littlebignormal_pusab": pygame.font.Font(
            "./ressources/polices/Pusab.ttf",
            35
        ),
        "determination_font": pygame.font.Font(
            "./ressources/polices/DeterminationMono.ttf",
            60
        ),
        "little_determination_font": pygame.font.Font(
            "./ressources/polices/DeterminationMono.ttf",
            30
        ),
        "littlebig_determination_font": pygame.font.Font(
            "./ressources/polices/DeterminationMono.ttf",
            40
        ),
        "littleshort_determination_font": pygame.font.Font(
            "./ressources/polices/DeterminationMono.ttf",
            36
        ),
    }
    return fonts


def init_texts(fonts):
    """
    Initialise les textes du jeu.
    """
    texts = {
        "spamton_meme": fonts["determination_font"].render(
            "SPAMTON DANCE",
            True,
            couleur["white"]
        ),
        "alphalaneous": fonts["littlenormal_pusab"].render(
            "Alphalaneous",
            True,
            couleur["gold"]
        ),
        "alphalaneous_desc1": fonts["normal_pusab"].render(
            "Pour certaines",
            True,
            couleur["gold"]
        ),
        "alphalaneous_desc2": fonts["normal_pusab"].render(
            "textures du jeu",
            True,
            couleur["gold"]
        ),
        "hiroshi": fonts["littlenormal_pusab"].render(
            "Hiroshi",
            True,
            couleur["gold"]
        ),
        "hiroshi_desc1": fonts["normal_pusab"].render(
            "Pour le logo",
            True,
            couleur["gold"]
        ),
        "hiroshi_desc2": fonts["normal_pusab"].render(
            "du jeu",
            True,
            couleur["gold"]
        ),
        "robtopgames": fonts["littlenormal_pusab"].render(
            "RobTop Games",
            True,
            couleur["gold"]
        ),
        "robtopgames_desc1": fonts["normal_pusab"].render(
            "Createur des",
            True,
            couleur["gold"]
        ),
        "robtopgames_desc2": fonts["normal_pusab"].render(
            "textures du jeu",
            True,
            couleur["gold"]
        ),
        "jouca": fonts["littlenormal_pusab"].render(
            "Jouca / Diego",
            True,
            couleur["gold"]
        ),
        "jouca_desc1": fonts["normal_pusab"].render(
            "Le developpeur",
            True,
            couleur["gold"]
        ),
        "jouca_desc2": fonts["normal_pusab"].render(
            "du jeu",
            True,
            couleur["gold"]
        ),
        "select_tries": fonts["big_pusab"].render(
            "Sélectionner le nombre d'essaies",
            True,
            couleur["gold"]
        ),
        "select_difficulty": fonts["big_pusab"].render(
            "Sélectionner la difficulté",
            True,
            couleur["gold"]
        ),
        "ok_info": fonts["littlebignormal_pusab"].render(
            ": couleur bien placée",
            True,
            couleur["gold"]
        ),
        "position_issue_info1": fonts["littlebignormal_pusab"].render(
            ": couleur présente",
            True,
            couleur["gold"]
        ),
        "position_issue_info2": fonts["littlebignormal_pusab"].render(
            "mais mal placée",
            True,
            couleur["gold"]
        ),
    }
    return texts


def init_buttons():
    """
    Initialise les boutons du jeu.
    """
    buttons = {
        "credits": Button(
            charger_ressource("./sprites/info.png"),
            [1220, 660, 50, 50]
        ),
        "returnMenu": Button(
            charger_ressource("./sprites/cross.png"),
            [20, 20, 50, 50]
        ),
        "returnMenuJeu": Button(
            charger_ressource("./sprites/cross.png"),
            [1200, 20, 50, 50]
        ),
        "returnMenuQuit": Button(
            charger_ressource("./sprites/cross.png"),
            [20, 20, 50, 50]
        ),
        "play": Button(
            charger_ressource("./sprites/play.png"),
            [530, 280, 220, 220]
        ),
        "10_tries": Button(
            charger_ressource("./sprites/10_essaies.png"),
            [400, 280, 220, 220]
        ),
        "12_tries": Button(
            charger_ressource("./sprites/12_essaies.png"),
            [680, 280, 220, 220]
        ),
        "facile": Button(
            charger_ressource("./sprites/facile.png"),
            [280, 280, 220, 220]
        ),
        "normal": Button(
            charger_ressource("./sprites/normal.png"),
            [540, 280, 220, 220]
        ),
        "difficile": Button(
            charger_ressource("./sprites/difficile.png"),
            [800, 280, 220, 220]
        ),
    }
    return buttons


def spamton_dance(var):
    """
    Permet de gérer l'animation de Spamton.
    """
    var["spamton_sprite"] = (var["spamton_sprite"] + 1) % 20
    value = str(var["spamton_sprite"])
    sprite = var["spamton_gif"].parse_sprite(f"spamton_troll{value}.png")
    return var, sprite


def explosion(var):
    """
    Permet de faire l'animation de l'explosion.
    """
    explosion_sound = pygame.mixer.Sound("./ressources/sounds/explosion.ogg")
    if var["explosion_fini"] == 0:
        var["explosion_delay"] = (var["explosion_delay"] + 1) % 2
        if var["explosion_delay"] == 1:
            var["explosion_sprite"] = (var["explosion_sprite"] + 1) % 17
            if var["explosion_sprite"] == 1:
                explosion_sound.play()
            value = str(var["explosion_sprite"])
            sprite = var["explosion_gif"].parse_sprite(f"explosion{value}.png")
            if var["explosion_sprite"] == 16:
                var["explosion_fini"] = 1
        else:
            value = str(var["explosion_sprite"])
            sprite = var["explosion_gif"].parse_sprite(f"explosion{value}.png")
    return var, sprite


def affichage_menu(menu, var, screen, clock):
    """
    Permet de gérer l'affichage des menus.
    """
    if menu == "principal":
        var = affichage_menu_principal(screen, var)
    elif menu == "select_tries":
        var = affichage_menu_select_tries(screen, var)
    elif menu == "select_difficulty":
        var = affichage_menu_select_difficulty(screen, var)
    elif menu == "jeu":
        var = affichage_menu_jeu(screen, var)
    elif menu == "credits":
        var = affichage_menu_credits(screen, var)
    elif menu == "secret_spamton":
        var = affichage_menu_spamton(screen, var)

    if var["debug"] == 1:
        screen.blit(update_fps(clock, var), (1220, 600))

    pygame.display.flip()
    return var


def affichage_menu_principal(screen, var):
    """
    Affiche le menu principal.
    """
    var["background_parallax"].draw(screen)
    screen.blit(
        pygame.transform.scale(
            charger_ressource("/sprites/mastermind_titre.png"),
            (838, 133)
        ),
        (220, 80)
    )
    code = var["fonts"]["determination_font"].render(
        var["secret_code"],
        True,
        couleur["green"]
    )
    terminal = var["fonts"]["determination_font"].render(
        ">",
        True,
        couleur["green"]
    )
    screen.blit(terminal, (30, 650))
    screen.blit(code, (70, 650))
    var["buttons"]["credits"].draw(screen)
    var["buttons"]["play"].draw(screen)
    var["buttons"]["returnMenuQuit"].draw(screen)
    return var


def affichage_menu_select_tries(screen, var):
    """
    Affiche le menu des sélections des essaies.
    """
    var["background_parallax"].draw(screen)
    screen.blit(var["texts"]["select_tries"], (120, 160))
    var["buttons"]["10_tries"].draw(screen)
    var["buttons"]["12_tries"].draw(screen)
    var["buttons"]["returnMenu"].draw(screen)
    return var


def affichage_menu_select_difficulty(screen, var):
    """
    Affiche le menu des difficultés.
    """
    var["background_parallax"].draw(screen)
    screen.blit(var["texts"]["select_difficulty"], (220, 160))
    var["buttons"]["facile"].draw(screen)
    var["buttons"]["normal"].draw(screen)
    var["buttons"]["difficile"].draw(screen)
    var["buttons"]["returnMenu"].draw(screen)
    return var


def affichage_menu_credits(screen, var):
    """
    Affiche le menu des crédits.
    """
    background = pygame.transform.scale(
        charger_ressource("/sprites/background1.png"),
        (1280, 1280)
    )
    screen.blit(background, (0, 0))
    screen.blit(
        pygame.transform.scale(
            charger_ressource("/sprites/credits.png"),
            (482, 123)
        ),
        (400, 40)
    )

    screen.blit(
        pygame.transform.scale(
            charger_ressource("/sprites/alphalaneous.png"),
            (150, 150)
        ),
        (100, 210)
    )
    screen.blit(var["texts"]["alphalaneous"], (60, 370))
    screen.blit(var["texts"]["alphalaneous_desc1"], (270, 270))
    screen.blit(var["texts"]["alphalaneous_desc2"], (270, 300))

    screen.blit(
        pygame.transform.scale(
            charger_ressource("/sprites/hiroshi.png"),
            (150, 150)
        ),
        (100, 410)
    )
    screen.blit(var["texts"]["hiroshi"], (115, 570))
    screen.blit(var["texts"]["hiroshi_desc1"], (270, 470))
    screen.blit(var["texts"]["hiroshi_desc2"], (270, 500))

    screen.blit(
        pygame.transform.scale(
            charger_ressource("/sprites/robtopgames.png"),
            (150, 150)
        ),
        (700, 210)
    )
    screen.blit(var["texts"]["robtopgames"], (660, 370))
    screen.blit(var["texts"]["robtopgames_desc1"], (870, 270))
    screen.blit(var["texts"]["robtopgames_desc2"], (870, 300))

    screen.blit(
        pygame.transform.scale(
            charger_ressource("/sprites/jouca.png"),
            (150, 150)
        ),
        (700, 410)
    )
    screen.blit(var["texts"]["jouca"], (670, 570))
    screen.blit(var["texts"]["jouca_desc1"], (870, 470))
    screen.blit(var["texts"]["jouca_desc2"], (870, 500))
    var["buttons"]["returnMenu"].draw(screen)
    return var


def affichage_menu_spamton(screen, var):
    """
    Affiche le menu secret de Spamton.
    """
    screen.fill(couleur["black"])
    var, sprite = spamton_dance(var)
    sprite = pygame.transform.scale(sprite, (400, 400))
    screen.blit(sprite, (450, 30))
    screen.blit(
        pygame.transform.scale(
            charger_ressource("/sprites/spamton_angel.png"),
            (150, 150)
        ),
        (1000, 80)
    )
    screen.blit(
        pygame.transform.flip(
            pygame.transform.scale(
                charger_ressource("/sprites/spamton_angel.png"),
                (150, 150)
            ),
            True,
            False
        ),
        (150, 80)
    )
    pygame.draw.rect(
        screen,
        couleur["white"],
        pygame.Rect(400, 25, 500, 500),
        2
    )
    screen.blit(var["texts"]["spamton_meme"], (485, 450))
    var["buttons"]["returnMenu"].draw(screen)
    return var


def affichage_menu_jeu(screen, var):
    """
    Affiche le jeu.
    """
    var["background_jeu_parallax"].draw(screen)
    if var["explosion_sprite"] < 12:
        var["grille"].draw(screen, var)
        pygame.draw.rect(
            screen,
            couleur["dark_brown"],
            pygame.Rect(750, 110, 500, 300)
        )
        pygame.draw.rect(
            screen,
            couleur["brown"],
            pygame.Rect(755, 115, 490, 290)
        )
        screen.blit(
            pygame.transform.scale(
                charger_ressource("/sprites/checkmark.png"),
                (55, 55)
            ),
            (765, 215)
        )
        screen.blit(var["texts"]["ok_info"], (830, 230))
        screen.blit(
            pygame.transform.scale(
                charger_ressource("/sprites/info.png"),
                (55, 55)
            ),
            (765, 300)
        )
        screen.blit(var["texts"]["position_issue_info1"], (830, 315))
        screen.blit(var["texts"]["position_issue_info2"], (870, 345))
        screen.blit(
            pygame.transform.scale(
                charger_ressource("/sprites/mastermind_titre.png"),
                (440, 72)
            ),
            (775, 120)
        )
        var["selection"].draw(screen)
        if var["gagné"] == 1:
            var["selection"].draw_win(screen, var)
        var["selection"].draw_checker(var)

        # Ecriture de la surface score
        score_surface_2 = pygame.Surface((205, 110))
        score_surface_2.fill(couleur["dark_brown"])
        score_surface = pygame.Surface((200, 100))
        score_surface.fill(couleur["brown"])
        screen.blit(score_surface_2, (550, 280))

        # Ecriture du score dans la surface
        score = var["fonts"]["littlebig_determination_font"].render(
            f"Score : {var['score']}",
            1,
            couleur["gold"]
        )
        text_rect = score.get_rect(center=score_surface.get_rect().center)
        score_surface.blit(score, (text_rect.x, text_rect.y))

        screen.blit(score_surface, (555, 285))
    elif var["explosion_sprite"] == 16:
        pygame.draw.rect(
            screen,
            couleur["dark_brown"],
            pygame.Rect(205, 235, 860, 310)
        )

        pygame.draw.rect(
            screen,
            couleur["brown"],
            pygame.Rect(210, 240, 850, 300)
        )

        screen.blit(
            pygame.transform.scale(
                charger_ressource("/sprites/gameover.png"),
                (752, 134)
            ),
            (250, 270)
        )

        score = var["fonts"]["determination_font"].render(
            f"Score : {var['score']}",
            1,
            couleur["gold"]
        )
        text_rect = score.get_rect(center=(var["width"]/2, 450))
        screen.blit(score, text_rect)
    if var["perdu"] != 1 and var["gagné"] != 1:
        var["selection"].draw_buttons(screen)
    var["buttons"]["returnMenuJeu"].draw(screen)
    if var["perdu"] == 1 and var["explosion_fini"] == 0:
        var, sprite = explosion(var)
        if sprite is not None:
            sprite = pygame.transform.scale(sprite, (700, 700))
            screen.blit(sprite, (-150, -150))
            screen.blit(sprite, (-150, 150))
            screen.blit(sprite, (300, -150))
            screen.blit(sprite, (650, 250))
            screen.blit(sprite, (700, -100))
    if var["debug"] == 1:
        text = var["fonts"]["little_determination_font"].render(
            str(var["code"]),
            True,
            couleur["red"]
        )
        text_rect = text.get_rect()
        setattr(text_rect, "topright", (1280, 680))
        screen.blit(text, text_rect)
    return var


def generer_jeu(var):
    """
    Génère les données de la partie du jeu.
    """
    var = generer_code(var)
    var["grille"] = Grille(var["nb_couleurs"], var["essaies"], var)
    var["selection"] = Selection(var)
    var["background_jeu_parallax"] = Parallax(
        f"background{random.randint(1, 12)}.png",
        4,
        False
    )
    return var


def secret_codes(var, menu):
    """
    Permet de gérer les secret codes du menu principal.
    """
    if var["secret_code"] == "SPAMTON":
        menu = "secret_spamton"
        var["secret_code"] = ""
        pygame.mixer.music.load("./ressources/sounds/spamton.ogg")
        pygame.mixer.music.play(-1)
    elif var["secret_code"] == "SUS":
        var["secret_code"] = ""
        sus = pygame.mixer.Sound("./ressources/sounds/sus.ogg")
        sus.play()
    elif var["secret_code"] == "GODMODE":
        var["secret_code"] = ""
        if var["godmode"] == 0:
            var["godmode"] = 1
        else:
            var["godmode"] = 0
    elif var["secret_code"] == "GASTER":
        var["jeu_en_cours"] = False
    elif var["secret_code"] == "DEBUG":
        var["secret_code"] = ""
        if var["debug"] == 0:
            var["debug"] = 1
        else:
            var["debug"] = 0
    elif len(var["secret_code"]) >= 10:
        var["secret_code"] = ""
    return var, menu


def generer_code(var):
    """
    Génère le code de couleurs par le nombre de couleurs donnée.
    """
    nb_couleurs = var["nb_couleurs"]
    while nb_couleurs != 0:
        var["code"].append(
            couleur_mastermind_ID[random.randint(1, var["nb_couleurs"])]
        )
        nb_couleurs -= 1
    return var


def controles_principal(menu, var, event):
    """
    Occupation des contrôles du menu principal.
    """
    if (
        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
    ) or var["buttons"]["returnMenu"].event_handler(event):
        var["jeu_en_cours"] = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            var["secret_code"] = var["secret_code"][0:-1]
        else:
            var["secret_code"] += (event.unicode).upper()
            var, menu = secret_codes(var, menu)
    elif var["buttons"]["credits"].event_handler(event):
        var["secret_code"] = ""
        menu = "credits"
    elif var["buttons"]["play"].event_handler(event):
        var["secret_code"] = ""
        menu = "select_difficulty"
    return menu, var


def controles_select_tries(menu, var, event):
    """
    Occupation des contrôles du menu des essaies.
    """
    if (
        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
    ) or var["buttons"]["returnMenu"].event_handler(event):
        menu = "select_difficulty"
    elif var["buttons"]["10_tries"].event_handler(event):
        menu = "jeu"
        var["essaies"] = 10
        var = generer_jeu(var)
    elif var["buttons"]["12_tries"].event_handler(event):
        var["essaies"] = 12
        menu = "jeu"
        var = generer_jeu(var)
    return menu, var


def controles_select_difficulty(menu, var, event):
    """
    Occupation des contrôles du menu des difficultés.
    """
    if (
        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
    ) or var["buttons"]["returnMenu"].event_handler(event):
        menu = "principal"
    elif var["buttons"]["facile"].event_handler(event):
        var["nb_couleurs"] = 4
        menu = "select_tries"
    elif var["buttons"]["normal"].event_handler(event):
        var["nb_couleurs"] = 5
        menu = "select_tries"
    elif var["buttons"]["difficile"].event_handler(event):
        var["nb_couleurs"] = 6
        menu = "select_tries"
    return menu, var


def controles_credits(menu, var, event):
    """
    Occupation des contrôles du menu des crédits.
    """
    if (
        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
    ) or var["buttons"]["returnMenu"].event_handler(event):
        menu = "principal"
    return menu, var


def controles_spamton(menu, var, event):
    """
    Occupation des contrôles du menu secret de Spamton.
    """
    if (
        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
    ) or var["buttons"]["returnMenu"].event_handler(event):
        pygame.mixer.music.stop()
        menu = "principal"
    return menu, var


def controles_jeu(menu, var, event):
    """
    Occupation des contrôles du jeu.
    """
    if (
        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
    ) or var["buttons"]["returnMenuJeu"].event_handler(event):
        var["perdu"] = 0
        var["gagné"] = 0
        var["grille"] = ""
        var["explosion_fini"] = 0
        var["explosion_sprite"] = 0
        var["code"] = []
        var["table"] = []
        var["score"] = 0
        var["essaies"] = 0
        var["triche_ensemble"] = []
        menu = "principal"
        return menu, var
    elif var["selection"]._rejouer.event_handler(event) and var["gagné"] == 1:
        var["perdu"] = 0
        var["gagné"] = 0
        var["grille"] = ""
        var["explosion_fini"] = 0
        var["explosion_sprite"] = 0
        var["code"] = []
        var["table"] = []
        var["triche_ensemble"] = []
        var = generer_jeu(var)
        menu = "jeu"
        return menu, var
    if var["perdu"] != 1 and var["gagné"] != 1:
        for i in range(var["nb_couleurs"]):
            if var["selection"]._buttons_haut[i].event_handler(event):
                var["selection"].change_couleur_haut(i)
            elif var["selection"]._buttons_bas[i].event_handler(event):
                var["selection"].change_couleur_bas(i)
        if var["selection"]._valider.event_handler(event) or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_t
        ):
            var["selection"].valider(var["grille"])
            var["selection"].check_validation(var["code"])
        validation_liste = var["selection"]._validation_liste
        if validation_liste["OK"] == var["nb_couleurs"]:
            var["gagné"] = 1
            var["score"] += 1
            victory = pygame.mixer.Sound("./ressources/sounds/victory.ogg")
            victory.play()
        elif 0 not in var["grille"]._table[-1]:
            var["perdu"] = 1
    return menu, var


def controles(var, menu):
    """
    Occupation de la gestion des contrôles par rapport à leur menu.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            var["jeu_en_cours"] = False

        if menu == "principal":
            menu, var = controles_principal(menu, var, event)
        elif menu == "select_tries":
            menu, var = controles_select_tries(menu, var, event)
        elif menu == "select_difficulty":
            menu, var = controles_select_difficulty(menu, var, event)
        elif menu == "jeu":
            menu, var = controles_jeu(menu, var, event)
        elif menu == "credits":
            menu, var = controles_credits(menu, var, event)
        elif menu == "secret_spamton":
            menu, var = controles_spamton(menu, var, event)
    return menu, var


def update_fps(clock, var):
    """
    Met à jour les FPS du jeu.
    """
    fps = str(int(clock.get_fps()))
    fps_text = var["fonts"]["determination_font"].render(
        fps,
        1,
        couleur["blue"]
    )
    return fps_text


def main():
    """
    Fonction principale du lancement du jeu.
    """
    screen = init_screen()

    menu = "principal"
    var = {
        "width": screen_size[0],
        "heigth": screen_size[1],
        "jeu_en_cours": True,
        "fonts": init_fonts(),
        "texts": init_texts(init_fonts()),
        "buttons": init_buttons(),
        "background_parallax": Parallax("background1.png", 4, False),
        "background_jeu_parallax": Parallax("background1.png", 4, False),
        "essaies": 0,
        "nb_couleurs": 4,
        "selection": "",
        "grille": "",
        "code": [],
        "table": [],
        "checker": [],
        "score": 0,
        "perdu": 0,
        "gagné": 0,
        "explosion_gif": Spritesheet('./ressources/sprites/explosion.png'),
        "explosion_sprite": 0,
        "explosion_delay": 0,
        "explosion_fini": 0,
        "secret_code": "",
        "spamton_gif": Spritesheet('./ressources/sprites/spamton_troll.png'),
        "spamton_sprite": 0,
        "godmode": 0,
        "debug": 0,
        "triche_ensemble": []
        }

    clock = pygame.time.Clock()
    frame_per_second = 60
    while var["jeu_en_cours"]:
        clock.tick(frame_per_second)

        var = affichage_menu(menu, var, screen, clock)
        menu, var = controles(var, menu)

    pygame.quit()


# --------------- DEMARRAGE --------------- #
main()
