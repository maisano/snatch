# -*- coding: utf-8 -*-

"""
snatch.models
~~~~~~~~~~~~~

ImageList class for snatch

:copyright: (c) 2013 by Richard Maisano.
:license: Apache 2.0, see LICENSE for more details.

"""

from .utils import extension_filter_maker

import re


REGEXP_NUMBER = re.compile(' *?(\d+)')


class ImageList(object):
    """Response :class:`ImageList <ImageList>` object.

    Iterable wrapper, filled with :class:`Image <Image>` objects, created
    from parsed HTTP response.
    """

    def __init__(self, images=None):
        self.images = images or []

    def __repr__(self):
        return '<ImageList [%s]>' % (self.count)

    def __nonzero__(self):
        """Returns True if len of :attr:`images` is > 0
        """
        return bool(self.images)

    def __bool__(self):
        """Returns True if len of :attr:`images` is > 0
        """
        return self.__nonzero__()

    def __iter__(self):
        """Returns iterable :attr:`images`
        """
        return iter(self.images)

    def __len__(self):
        """Returns count of :attr:`images`
        """
        return len(self.images)

    def __getitem__(self, i):
        """Proxy to :attr:`images`
        """
        return self.images[i]

    def __contains__(self, item):
        """Checks to see if :class:`Image <Image>` object with matching
        src already exists in :attr:`images`.
        """
        srcs = [i.src for i in iter(self)]
        return item.src in srcs

    def append(self, image):
        """Proxy to :attr:`images`
        When an image with the same :attr:`src` currently exists,
        ``append`` simply increments that :class:`Image <Image>`'s object
        :attr:`count` by 1.
        """
        if not isinstance(image, Image):
            raise ValueError("ImageList objects can only append Image objects")

        if image not in self:
            self.images.append(image)

        else:
            for i in iter(self):
                if i.src == image.src:
                    i.count += 1
                    break

    def with_extension(self, extensions):
        """Returns a new :class:`ImageList` object, with :attr:`images`
        filtered by extension.
        """
        if isinstance(extensions, basestring):
            extensions = [extensions]
        elif not isinstance(extensions, (tuple, list)):
            raise ValueError('"extensions" passed in must be a string, tuple or list')

        extension_filter = extension_filter_maker(extensions)
        images = extension_filter(self.images)
        return ImageList(images)

    @property
    def count(self):
        """Returns length of self.images
        """
        return len(self.images)

    @property
    def urls(self):
        """Returns list of :attr:`src` values for each image in :attr:`images`
        """
        return [i.src for i in iter(self)]

    @property
    def extensions(self):
        """Returns unique list of extensions from the :attr:`extension`
        properties in :attr:`images`
        """
        extensions = []
        for image in iter(self):
            ext = image.extension
            if ext not in extensions:
                extensions.append(ext)
        return extensions


class Image(object):
    """Convenience :class:`Image <Image>` object.
    To be contained within :class:`ImageList <ImageList>`.

    Pretty much exists to make the API a little nicer.
    """
    def __init__(self, attrs):
        for k, v in attrs.iteritems():

            if k in ('width', 'height') and v is not None:
                try:
                    v = int(v)
                except ValueError:
                    match = REGEXP_NUMBER.match(v)
                    if match:
                        v = int(match.group())

            setattr(self, k, v)

        self.count = 1

    def __repr__(self):
        return '<Image ["%s"]>' % (self.filename)

    def __iter__(self):
        """Returns iterable :attr:`__dict__`.
        """
        return self.__dict__.iteritems()

    @property
    def filename(self):
        """Returns parsed filename of image.
        """
        return self.src.rsplit('/', 1)[1]

    @property
    def extension(self):
        """Returns parsed file extension of :class:`Image <Image>`'s
        :attr:`src`.
        """
        return self.filename.rsplit('.', 1)[1].lower()

    @property
    def url(self):
        """Proxy property to :attr:`src`.
        """
        return self.src
