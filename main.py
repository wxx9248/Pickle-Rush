#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import pygame

from audio.AudioThread import AudioThread
from config.ConfigMonitorThread import ConfigMonitorThread
from event.EventDispatcher import EventDispatcher
from event.EventHandler import EventHandler
from input.InputHandlingThread import InputHandlingThread

running = True


def stop(_):
    global running
    running = False


def main():
    # Logger setup
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s][%(levelname)s][%(name)s] %(message)s")
    logger = logging.getLogger()

    # Pygame setup
    pygame.init()

    # Event dispatcher initialization
    event_dispatcher = EventDispatcher()
    event_dispatcher.register(pygame.QUIT, "root", EventHandler("quit", stop))

    # Start all subsystems
    threads = [
        ConfigMonitorThread(event_dispatcher, "config.json"),
        AudioThread(event_dispatcher),
        InputHandlingThread(event_dispatcher)
    ]

    for thread in threads:
        logger.info(f"Starting {thread}")
        thread.start()

    screen = pygame.display.set_mode((600, 600))
    while running:
        event_dispatcher.dispatch_all(pygame.event.get())
        pygame.display.update()

    while len(threads):
        thread = threads.pop()
        thread.join()
        logger.info(f"{thread} quit")


if __name__ == '__main__':
    main()
