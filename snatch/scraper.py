# -*- coding: utf-8 -*-

"""
snatch.parser
~~~~~~~~~~~~~

ImageScraper object for snatch

:copyright: (c) 2013 by Richard Maisano.
:license: Apache 2.0, see LICENSE for more details.

"""

from .events import EventsMixin, trigger_event
from .models import ImageList, Image
from .utils import extension_filter_maker

import requests

from urlparse import urljoin

from bs4 import BeautifulSoup


class ImageScraper(EventsMixin):
    """Internal :class:`ImageScraper <ImageScraper>` object.

    For parsing HTML and formatting images scraped from URL
    """

    def __init__(self, with_extension=None, duplicates=None, callbacks=None, headers=None):
        """Init method for internal :class:`ImageScraper <ImageScraper>` object.

        :param with_extension: list of file extensions to filter results by
        :type with_extension: tuple, list

        :param callbacks: key-value pair of events and callables to trigger
        :type callbacks: dict
        """

        super(ImageScraper, self).__init__()

        if with_extension is not None:
            if isinstance(with_extension, basestring):
                with_extension = [with_extension]
            if not isinstance(with_extension, (tuple, list)):
                raise ValueError('"with_extension" kwarg must be a string, tuple or list')

            extensions_filter = extension_filter_maker(with_extension)
            self.add_callback('complete', extensions_filter)

        if callbacks is not None:
            if not isinstance(callbacks, dict):
                raise ValueError('"callbacks" kwarg must be a dict')

            for event, callback in callbacks.iteritems():
                self.add_callback(event, callback)

    def get_images(self, url, headers=None):
        """Constructs and returns :class:`ImageList <ImageList>` object

        :param url: URL to scrape
        :param headers: dict of headers to pass into request object
        """

        headers = headers or {}
        html = requests.get(url, headers=headers).content

        soup = BeautifulSoup(html, 'lxml')

        base = soup.find('base')
        base = base.get('href') if base else url

        images = ImageList()

        for image in soup.find_all('img'):
            src = image.get('src')

            if not src:
                continue

            i = Image({
                'src': urljoin(base, src),
                'width': image.get('width'),
                'height': image.get('height'),
                'title': image.get('title'),
                'alt': image.get('alt')
            })
            images.append(i)

        images = trigger_event('complete', self.callbacks, images)

        return images
