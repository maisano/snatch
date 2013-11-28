# -*- coding: utf-8 -*-

"""
snatch.events
~~~~~~~~~~~~~

Events implementation details for snatch, where you can further manipulate
the image data scraped from the request.

Inspired by the hooks module within Kenneth Reitz' Requests library.
<https://github.com/kennethreitz/requests>

Available events:

``complete``:
    After inital images list has been constructed

:copyright: (c) 2013 by Richard Maisano
:license: Apache 2.0, see LICENSE for more details

"""

from .models import ImageList

from collections import Callable


class EventsMixin(object):
    """Internal :class:`EventsMixin` object.

    For mixing in event registration/binding methods
    """
    EVENTS = ['complete']

    def __init__(self):
        super(EventsMixin, self).__init__()
        self.callbacks = {event:[] for event in self.EVENTS}

    def add_callback(self, event, hook):
        """Hook registration for subclassed objects

        :param event: name of event to bind callback to
        :type event: string
        :param hook: function to bind as event callback
        :type hook: function/callable
        """

        if event not in self.callbacks:
            raise ValueError('Unsupported event type "%s"' % (event))

        if isinstance(hook, Callable):
            self.callbacks[event].append(hook)
        elif hasattr(hook, '__iter__'):
            self.callbacks[event].extend(h for h in hook if isinstance(h, Callable))


def trigger_event(event, callbacks, images):
    """Helper fn to call hooks

    :param event: String, name of event to trigger
    :param callbacks: Dict, hash of events and callables
    :param images: List of dicts, attrs of scraped images
    """

    if event not in callbacks:
        raise ValueError('Unsupported event type "%s"' % (event))

    for hook in callbacks[event]:

        hook_response = hook(images)

        if hook_response is not None:
            images = hook_response

    return ImageList([i for i in images])
