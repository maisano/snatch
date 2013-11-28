# -*- coding: utf-8 -*-

"""
snatch.api
~~~~~~~~~~

Snatch API implementation

:copyright: (c) 2013 by Richard Maisano.
:license: Apache 2.0, see LICENSE for more details.

"""

from .scraper import ImageScraper


def snatch(url, **kwargs):
    """Constructs and sends a :class:`Snatch <Snatch>`.
    Returns :class:`Snatched <Snatched>` object.

    :param url: URL for the :class:`Snatch` object
    :param with_extension: (optional) Tuple of accepted extensions
    :param callbacks: (optional) Dict, hash of events and callables
    :param headers: (optional) Dict, hash of headers to pass into request object
    """
    headers = kwargs.pop('headers', {})
    scraper = ImageScraper(**kwargs)
    return scraper.get_images(url, headers)
