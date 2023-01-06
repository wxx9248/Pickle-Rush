# -*- coding: utf-8 -*-
import json

import pygame

from core.object_model.Sprite import Sprite
from util import util


class Text(Sprite):
    def __init__(self, definition_file_path: str, *groups: pygame.sprite.AbstractGroup):
        definition = json.load(open(definition_file_path))
        self.__wrap = definition["wrap"]
        self.__font = definition["font"]
        self.__font_size = definition["fontSize"]
        self.__bold = definition["bold"]
        self.__italic = definition["italic"]
        self.__color = definition["color"]
        self.__background_color = definition["backgroundColor"]
        self.__content = definition["content"]

        if self.__wrap is None:
            super().__init__(self.freeform_renderer().convert_alpha(), *groups)
            return

        if self.__wrap == "word":
            self.__box_size_width = definition["boxSize"]["width"]
            self.__box_size_height = definition["boxSize"]["height"]
            super().__init__(self.word_wrapped_renderer().convert_alpha(), *groups)
            return

        raise NotImplementedError(f"Unsupported wrapping method {self.__wrap}")

    def freeform_renderer(self) -> pygame.surface.Surface:
        font_object = util.text_render_get_font_object(self.__font, self.__font_size, self.__bold, self.__italic)
        font_height = font_object.get_height()

        lines = self.__content.split('\n')
        line_surfaces = [font_object.render(line, True, self.__color) for line in lines]
        surface_width = max([line_surface.get_width() for line_surface in line_surfaces])
        surface_height = len(lines) * font_height
        surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA, 32)
        if self.__background_color is not None:
            surface.fill(pygame.Color(self.__background_color))

        cursor = [0, 0]
        for line_surface in line_surfaces:
            surface.blit(line_surface, cursor)
            util.text_render_new_line(cursor, font_height)

        return surface

    def word_wrapped_renderer(self) -> pygame.surface.Surface:
        """
         Wrap the text into the space of the rect, using the font object provided.
         Returns a surface of rect size with the text rendered in it.
        """
        font_object = util.text_render_get_font_object(self.__font, self.__font_size, self.__bold, self.__italic)
        font_height = font_object.get_height()
        font_space_width = font_object.render(' ', False, pygame.Color("black")).get_width()

        surface = pygame.Surface((self.__box_size_width, self.__box_size_height), pygame.SRCALPHA, 32)
        if self.__background_color is not None:
            surface.fill(pygame.Color(self.__background_color))

        # Relative coordinate in wrapped_surface
        cursor = [0, 0]
        for line in self.__content.split('\n'):
            # Check if there is enough space for a single line
            if cursor[1] + font_height > self.__box_size_height:
                break

            for index, word in enumerate(line.split(' ')):
                word_surface = font_object.render(word, True, self.__color)
                word_surface_width = word_surface.get_width()

                # We don't need to continue if a single word cannot fit in the box
                if word_surface_width > self.__box_size_width:
                    return surface

                space_width = 0
                # If it is not the first word in a line, add a space
                if index:
                    space_width = font_space_width

                if cursor[0] + word_surface_width + space_width < self.__box_size_width:
                    # No need to wrap. Just add a space (if there is one) before printing
                    cursor[0] += space_width
                else:
                    # Need to wrap the line, so check if there is enough space for another line
                    if cursor[1] + 2 * font_height >= self.__box_size_height:
                        # We don't have enough space, so abort rendering
                        return surface
                    # OK to wrap and continue rendering
                    util.text_render_new_line(cursor, font_height)

                # Print the word
                surface.blit(word_surface, cursor)
                # Move cursor correspondingly
                cursor[0] += word_surface_width

            # Handle newline characters
            util.text_render_new_line(cursor, font_height)

        return surface
