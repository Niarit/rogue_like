"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod
import pygame.mixer as play_music

import color
from engine import Engine
import entity_factories
import input_handler
from game_map import GameWorld

# Load the background image and remove the alpha channel.
background_image = tcod.image.load("menu_background.png")[:, :, :3]


class Boo(input_handler.BaseEventHandler):
    def on_render(self, console: tcod.Console) -> None:

        play_music.init()
        play_music.music.load("music/credits.wav")
        play_music.music.set_volume(0.2)
        play_music.music.play()

        console.print(
            console.width // 2,
            console.height // 2 - 10,
            "ENJOY!",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        menu_width = console.width // 4

        for i, text in enumerate(
                ["      $  @  &",
                 "\n",
                 "Press [ESCAPE] if you want to go back to the main menu",
                 "\n",
                 "Written by: Niarit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(
            self, event: tcod.event.KeyDown
    ) -> Optional[input_handler.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            play_music.music.stop()
            return MainMenu()
        return None


class SecretHandler(input_handler.BaseEventHandler):
    def on_render(self, console: tcod.Console) -> None:

        console.print(
            console.width // 2,
            console.height // 2 - 10,
            "SECRET",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        menu_width = console.width // 4

        for i, text in enumerate(
                ["Hey, you found your first secret in this game! Good job!",
                 "\n",
                 "There will be a lot other secrets to find in this game,",
                 "(I promise I will implement them sometime) but for now that's all I can give.",
                 "\n",
                 "As a reward for finding this secret I wrote a song just for you!",
                 "Press [P] to check it out!",
                 "To go back to the main menu press [ESCAPE]",
                 "\n",
                 "Your friend: Nia"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(
            self, event: tcod.event.KeyDown
    ) -> Optional[input_handler.BaseEventHandler]:
        if event.sym == tcod.event.K_p:
            return Boo()
        elif event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            return MainMenu()
        return None


class HowToPlay(input_handler.BaseEventHandler):
    def on_render(self, console: tcod.Console) -> None:

        console.print(
            console.width // 2,
            console.height // 2 - 10,
            "HOW TO PLAY",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        menu_width = console.width // 4

        for i, text in enumerate(
                ["UP ARROW........move up",
                 "\n",
                 "DOWN ARROW......move down",
                 "\n",
                 "RIGHT ARROW.....move right",
                 "\n",
                 "LEFT ARROW......move left",
                 "\n",
                 "ESCAPE..........exit game",
                 "\n",
                 "KEY V...............open history",
                 "\n",
                 "KEY G...............pick up item",
                 "\n",
                 "KEY D...............drop item",
                 "\n",
                 "KEY I...............open inventory",
                 "\n",
                 "KEY C...............open character tab",
                 "\n",
                 "KEY L...............toggle look around",
                 "\n",
                 "KEY Y...............use stairs"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(
            self, event: tcod.event.KeyDown
    ) -> Optional[input_handler.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            return MainMenu()
        return None


def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""
    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        map_width=map_width,
        map_height=map_height,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
    )
    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
    )
    stick = copy.deepcopy(entity_factories.stick)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)

    stick.parent = player.inventory
    leather_armor.parent = player.inventory

    player.inventory.items.append(stick)
    player.equipment.toggle_equip(stick, add_message=False)

    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)

    return engine


def load_game(filename: str) -> Engine:
    """Load an Engine from a saved file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine


class MainMenu(input_handler.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "CRADLE OF AIN",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By Niarit",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
                ["[N] Play a new game", "[C] Continue last game", "[H] How to play", "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(
            self, event: tcod.event.KeyDown
    ) -> Optional[input_handler.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                return input_handler.MainGameEventHandler(load_game("saved_game.sav"))
            except FileNotFoundError:
                return input_handler.PopupMessage(self, "No saved game were found")
            except Exception as exc:
                traceback.print_exc()
                return input_handler.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.K_n:
            return input_handler.MainGameEventHandler(new_game())
        elif event.sym == tcod.event.K_h:
            return HowToPlay()
        elif event.sym == tcod.event.K_s:
            return SecretHandler()

        return None
