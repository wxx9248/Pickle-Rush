#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import pygame

from asset.AssetObjectFactory import AssetObjectFactory
from config.ConfigMonitorThread import ConfigMonitorThread
from config.JSONConfigManager import JSONConfigManager
from core.Stage import Stage
from event.CustomEventTypes import CustomEventTypes
from event.EventDispatcher import EventDispatcher
from event.EventHandler import EventHandler
from game.scene.Menu import Menu

_running = True


def stop(logger: logging.Logger):
    logger.info("Stopping main thread loop")
    global _running
    _running = False


def change_scene(scene_key: str):
    pass


def main():
    # Logger setup
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s][%(levelname)s][%(name)s] %(message)s")
    logger = logging.getLogger()

    logger.debug("Initializing pygame")
    pygame.init()

    logger.debug("Initializing config manager")
    config_manager = JSONConfigManager("config.json", JSONConfigManager.BindingMode.DOUBLE)

    logger.debug("Creating display surface")
    display_surface = pygame.display.set_mode(
        (config_manager.get("config.graphics.resolution.width"),
         config_manager.get("config.graphics.resolution.height"))
    )

    logger.debug("Initializing asset object factory")
    asset_object_factory = AssetObjectFactory()

    logger.debug("Initializing stage")
    stage = Stage(display_surface)

    logger.debug("Setting starting scene")
    stage.scene = Menu(display_surface.get_size(), asset_object_factory)

    logger.debug("Initializing event dispatcher")
    event_dispatcher = EventDispatcher()
    event_dispatcher.register(pygame.QUIT, "root", EventHandler("quit", lambda _: stop(logger)))
    event_dispatcher.register(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST, "root",
                              EventHandler("change-scene-request", lambda e: change_scene(e.scene_key)))
    event_dispatcher.register(pygame.KEYDOWN, "root", EventHandler("key-down", lambda e: stage.accept_input_event(e)))
    event_dispatcher.register(pygame.KEYUP, "root", EventHandler("key-up", lambda e: stage.accept_input_event(e)))

    logger.debug("Creating subsystem thread instances")
    config_monitor_thread = ConfigMonitorThread(event_dispatcher, config_manager)

    # Starting subsystem threads
    threads = [
        config_monitor_thread
    ]

    for thread in threads:
        logger.debug(f"Starting {thread}")
        thread.start()

    # Some operating systems will have problems rendering graphics and dispatching events
    # in threads other than the main thread, so handling global events and rendering here.
    clock = pygame.time.Clock()
    fps = config_manager.get("config.graphics.fps")
    while _running:
        event_dispatcher.dispatch_all(pygame.event.get())
        stage.scene.update()
        stage.scene.render(display_surface)
        pygame.display.update()
        clock.tick(fps)

    while len(threads):
        thread = threads.pop()
        thread.join()
        logger.debug(f"{thread} quit")


if __name__ == '__main__':
    main()
