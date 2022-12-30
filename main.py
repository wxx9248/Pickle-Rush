#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import pygame

from asset.AssetObjectFactory import AssetObjectFactory
from config.ConfigMonitorThread import ConfigMonitorThread
from config.JSONConfigManager import JSONConfigManager
from event.EventDispatcher import EventDispatcher
from event.EventHandler import EventHandler
from game.GameThread import GameThread
from input.InputHandlingThread import InputHandlingThread

_running = True


def stop(logger: logging.Logger):
    logger.info("Stopping main thread loop")
    global _running
    _running = False


def main():
    # Logger setup
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s][%(levelname)s][%(name)s] %(message)s")
    logger = logging.getLogger()

    logger.debug("Initializing pygame")
    pygame.init()

    logger.debug("Creating display surface")
    display_surface = pygame.display.set_mode((1280, 720))

    logger.debug("Initializing asset object factory")
    asset_object_factory = AssetObjectFactory()

    logger.debug("Initializing event dispatcher")
    event_dispatcher = EventDispatcher()
    event_dispatcher.register(pygame.QUIT, "root", EventHandler("quit", lambda _: stop(logger)))

    logger.debug("Initializing config manager")
    config_manager = JSONConfigManager("config.json", JSONConfigManager.BindingMode.DOUBLE)

    logger.debug("Creating subsystem thread instances")
    config_monitor_thread = ConfigMonitorThread(event_dispatcher, config_manager)
    input_handling_thread = InputHandlingThread(event_dispatcher)
    game_thread = GameThread(event_dispatcher, display_surface)

    # Starting subsystem threads
    threads = [
        config_monitor_thread,
        input_handling_thread,
        game_thread
    ]

    for thread in threads:
        logger.info(f"Starting {thread}")
        thread.start()

    # Some operating systems will have problems rendering graphics and dispatching events
    # in threads other than the main thread, so handling global events and rendering here.
    while _running:
        event_dispatcher.dispatch_all(pygame.event.get())
        not game_thread.render_queue.empty() and pygame.display.update(game_thread.render_queue.get())

    while len(threads):
        thread = threads.pop()
        thread.join()
        logger.info(f"{thread} quit")


if __name__ == '__main__':
    main()
