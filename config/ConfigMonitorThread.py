# -*- coding: utf-8 -*-

import pygame.event
import watchdog.events
import watchdog.observers

from config.AbstractConfigManager import AbstractConfigManager
from config.JSONConfigManager import JSONConfigManager
from core.BaseThread import BaseThread
from core.CustomEventTypes import CustomEventTypes


# TODO: Thread-safe support for concurrent writing to config dict and config file
#   Considering using a RWLock to protect dict and file

# TODO: Reminder: There also may be a performance issue if too many write operations happen at one time.
#   Considering caching those operations with an event queue if needs very frequent write operation.

# TODO: Use events for thread communication

class ConfigFileEventHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self):
        super().__init__()

    def on_modified(self, event: watchdog.events.FileSystemEvent):
        if not event.is_directory:
            pygame.event.post(pygame.event.Event(CustomEventTypes.EVENT_CONFIG_FILE_UPDATED))


class ConfigMonitorThread(BaseThread):
    def __init__(self, path: str):
        super().__init__()
        self.__path = path
        self.__config_manager: AbstractConfigManager = JSONConfigManager(self.__path,
                                                                         JSONConfigManager.BindingMode.DOUBLE)
        self.__file_observer: watchdog.observers.Observer = watchdog.observers.Observer()

    def run(self):
        self.event_dispatcher.register(
            CustomEventTypes.EVENT_CONFIG_FILE_UPDATED,
            lambda e: self.on_config_file_updated(e))

        self.event_dispatcher.register(
            CustomEventTypes.EVENT_CONFIG_DICT_UPDATED,
            lambda e: self.on_config_dict_updated(e))

        self.__file_observer.schedule(ConfigFileEventHandler(), self.__path)
        self.__file_observer.start()

        while self.running:
            self.event_dispatcher.dispatch_all(pygame.event.get())

        self.__file_observer.stop()
        self.__file_observer.join()

    def on_config_file_updated(self, _: pygame.event.Event):
        # Update config dict correspondingly
        self.logger.info("Detected config file changes. Loading new configuration...")
        self.__config_manager.sync_from_file()

    def on_config_dict_updated(self, _: pygame.event.Event):
        # Update config file correspondingly
        self.logger.info("Syncing new configuration to config file...")
        self.__config_manager.sync_to_file()
