# -*- coding: utf-8 -*-
import pygame.event


class CustomEventTypes:
    """
    Defines type constants for custom pygame events.

    Note:
    * Names of all event types must start with `EVENT_`, or the event will not be assigned with a proper event type ID.
    * The initial value of an event type ID can be anything. The value will be overridden after the module is imported.
    """
    EVENT_THREAD_EXCEPTION: int = None
    EVENT_CONFIG_DICT_UPDATED: int = None
    EVENT_CONFIG_FILE_UPDATED: int = None
    EVENT_STAGE_CHANGE_SCENE: int = None


# Executed when first imported
_imported = False
if not _imported:
    for event_type in CustomEventTypes.__dict__:
        if event_type.startswith("EVENT_"):
            setattr(CustomEventTypes, event_type, pygame.event.custom_type())
else:
    _imported = True
