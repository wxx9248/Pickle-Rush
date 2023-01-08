#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import pygame

from asset.AssetObjectFactory import AssetObjectFactory
from config.ConfigMonitorThread import ConfigMonitorThread
from config.JSONConfigManager import JSONConfigManager
from core.object_model.Stage import Stage
from event.CustomEventTypes import CustomEventTypes
from event.EventDispatcher import EventDispatcher
from event.EventHandler import EventHandler
from game.scene.Menu import Menu
from util.FrameRateStabilizer import FrameRateStabilizer

_running = True


def stop(logger: logging.Logger):
    logger.debug("Stopping main thread loop")
    global _running
    _running = False


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

    logger.debug("Initializing stage")
    stage = Stage(display_surface)

    logger.debug("Setting starting scene")
    stage.scene = Menu(display_surface.get_size())

    logger.debug("Initializing frame rate stabilizer")
    target_fps = config_manager.get("config.graphics.fps")
    frame_rate_stabilizer = FrameRateStabilizer(target_fps)
    next(frame_rate_stabilizer.get_tick)

    logger.debug("Initializing event dispatcher")
    event_dispatcher = EventDispatcher()
    event_dispatcher.register(pygame.QUIT, "root", EventHandler("quit", lambda _: stop(logger)))
    event_dispatcher.register(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST, "root",
                              EventHandler("change-scene-request", lambda e: stage.set_scene(e.scene)))
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

    clock = pygame.time.Clock()

    while _running:
        event_dispatcher.dispatch_all(pygame.event.get())
        stage.scene.update()
        stage.scene.render(display_surface)
        pygame.display.update()
        tick = frame_rate_stabilizer.get_tick.send(clock.get_fps())
        clock.tick(tick)

    while len(threads):
        thread = threads.pop()
        thread.join()
        logger.debug(f"{thread} quit")


if __name__ == '__main__':
    main()
