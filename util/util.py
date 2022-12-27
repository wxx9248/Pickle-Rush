# -*- coding: utf-8 -*-
import traceback
import typing


def catch_exception_and_print(f: typing.Callable):
    try:
        f()
    except Exception as e:
        traceback.print_exception(e)
