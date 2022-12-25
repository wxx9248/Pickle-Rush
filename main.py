#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import pygame

from config.ConfigMonitorThread import ConfigMonitorThread


def main():
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s][%(levelname)s][%(name)s] %(message)s")
    logger = logging.getLogger()

    pygame.init()

    threads = [ConfigMonitorThread("config.json")]

    for thread in threads:
        logger.info(f"Starting {thread}")
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
