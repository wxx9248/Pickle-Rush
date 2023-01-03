# -*- coding: utf-8 -*-
import json
import typing

import pygame

from core.object_model.Sprite import Sprite


class Text(Sprite):
    def __init__(self, definition_file_path: str, *groups: pygame.sprite.AbstractGroup):
        definition = json.load(open(definition_file_path))
        self.__box_size_width = definition["boxSize"]["width"]
        self.__box_size_height = definition["boxSize"]["height"]
        self.__font = definition["font"]
        self.__font_size = definition["fontSize"]
        self.__bold = definition["bold"]
        self.__italic = definition["italic"]
        self.__color = definition["color"]
        self.__background_color = definition["backgroundColor"]
        self.__content = definition["content"]

        super().__init__(self.render_text_surface(), *groups)

    def get_font_object(self) -> pygame.font.Font:
        font_fallback: typing.Optional[str] = None

        if type(self.__font) is str:
            font_fallback = self.__font
            if font_fallback == "default":
                font_fallback = pygame.font.get_default_font()
        elif type(self.__font) is list:
            preferences = [f.lower().replace(' ', '') for f in self.__font]
            available = pygame.font.get_fonts()
            font_fallback = ",".join([a for a in available for p in preferences if a.startswith(p)])
            if len(font_fallback) == 0:
                font_fallback = None

        return pygame.font.SysFont(font_fallback, self.__font_size, self.__bold, self.__italic)

    def render_text_surface(self) -> pygame.surface.Surface:
        """
         Wrap the text into the space of the rect, using the font object provided.
         Returns a surface of rect size with the text rendered in it.
        """
        surface = pygame.Surface((self.__box_size_width, self.__box_size_height), pygame.SRCALPHA, 32)
        if self.__background_color is not None:
            surface.fill(pygame.Color(self.__background_color))
        font_object = self.get_font_object()

        # Relative coordinate in wrapped_surface
        cursor = [0, 0]

        font_space_width = font_object.render(' ', False, pygame.Color("black")).get_width()
        font_height = font_object.get_height()

        def new_line():
            # Carriage return
            cursor[0] = 0
            # Line feed
            cursor[1] += font_height

        for line in self.__content.split('\n'):
            # First assume this line will take one-line space to fit
            if cursor[1] + font_height < self.__box_size_height:
                for index, word in enumerate(line.split(' ')):
                    word_surface = font_object.render(word, True, self.__color)
                    word_width = word_surface.get_width()

                    space_width = 0
                    # If it is not the first word in a line, add a space
                    if index:
                        space_width = font_space_width

                    if cursor[0] + word_width + space_width < self.__box_size_width:
                        # No need to wrap. Just add a space (if there is one) before printing
                        cursor[0] += space_width
                    else:
                        # Need to wrap the line, so check if there is enough space for another line
                        if cursor[1] + 2 * font_height >= self.__box_size_height:
                            # We don't have enough space, so abort rendering
                            return surface
                        # OK to wrap and continue rendering
                        new_line()

                    # Print the word
                    surface.blit(word_surface, cursor)
                    # Move cursor correspondingly
                    cursor[0] += word_width

                # Handle newline characters
                new_line()

        return surface
