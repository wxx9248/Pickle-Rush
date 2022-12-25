#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import pygame

from config.ConfigMonitorThread import ConfigMonitorThread
from event.EventDispatcher import EventDispatcher
from event.EventThread import EventThread


def main():
    # Logger setup
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s][%(levelname)s][%(name)s] %(message)s")
    logger = logging.getLogger()

    # Pygame setup
    pygame.init()

    # Event dispatcher initialization
    event_dispatcher = EventDispatcher()

    # Start all subsystems
    threads = [EventThread(event_dispatcher), ConfigMonitorThread(event_dispatcher, "config.json")]

    for thread in threads:
        logger.info(f"Starting {thread}")
        thread.start()

    for thread in threads:
        thread.join()
        logger.info(f"{thread} quit")


if __name__ == '__main__':
    main()
