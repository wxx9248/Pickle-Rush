# -*- coding: utf-8 -*-

import pygame.event
import watchdog.events
import watchdog.observers

from config.AbstractConfigManager import AbstractConfigManager
from config.JSONConfigManager import JSONConfigManager
from core.SubsystemThread import SubsystemThread
from event.CustomEventTypes import CustomEventTypes
from event.EventDispatcher import EventDispatcher
from event.EventHandler import EventHandler


# TODO: Reminder: There also may be a performance issue if too many write operations happen at one time.
#   Considering caching those operations with an event queue if needs very frequent write operation.


class WatchdogEventAdapter(watchdog.events.FileSystemEventHandler):
    def on_modified(self, event: watchdog.events.FileSystemEvent):
        if not event.is_directory:
            pygame.event.post(pygame.event.Event(CustomEventTypes.EVENT_CONFIG_FILE_UPDATED))


def post_event_dict_changed(node, key, value):
    event = pygame.event.Event(CustomEventTypes.EVENT_CONFIG_DICT_UPDATED)
    event.node = node
    event.key = key
    event.value = value
    pygame.event.post(event)


class ConfigMonitorThread(SubsystemThread):
    def __init__(self, global_event_dispatcher: EventDispatcher, path: str):
        super().__init__(global_event_dispatcher)

        self.logger.debug(f"Using config file in {path}")
        self.__path = path

        self.logger.debug(f"Creating config manager")
        self.__config_manager: AbstractConfigManager = JSONConfigManager(
            self.__path,
            JSONConfigManager.BindingMode.DOUBLE)

        self.logger.debug(f"Setting up hooks for config manager")
        self.__config_manager.after_update = post_event_dict_changed

        self.logger.debug(f"Setting up watchdog observer")
        self.__file_observer: watchdog.observers.Observer = watchdog.observers.Observer()

        self.logger.debug(f"Setting up event handlers")
        self.__event_handler_config_file_updated = \
            EventHandler("config-file-updated", lambda e: self.on_config_file_updated(e))
        self.__event_handler_config_dict_updated = \
            EventHandler("config-dict-updated", lambda e: self.on_config_dict_updated(e))

    def before_looper(self):
        self.logger.debug(f"Registering event handlers")
        self.local_event_dispatcher.register(
            CustomEventTypes.EVENT_CONFIG_FILE_UPDATED, self.name, self.__event_handler_config_file_updated)
        self.local_event_dispatcher.register(
            CustomEventTypes.EVENT_CONFIG_DICT_UPDATED, self.name, self.__event_handler_config_dict_updated)

        self.logger.debug(f"Starting watchdog observer")
        self.__file_observer.schedule(WatchdogEventAdapter(), self.__path)
        self.__file_observer.start()

    def after_looper(self):
        self.logger.debug(f"Stopping watchdog observer")
        self.__file_observer.stop()

    def on_config_file_updated(self, _: pygame.event.Event):
        # Update config dict correspondingly
        self.logger.info("Detected config file changes. Loading new configuration...")
        self.__config_manager.sync_from_file()
        self.logger.debug(self.__config_manager.config)

    def on_config_dict_updated(self, _: pygame.event.Event):
        # Update config file correspondingly
        self.logger.info("Syncing new configuration to config file...")
        self.__config_manager.sync_to_file()
