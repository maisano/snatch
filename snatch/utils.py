# -*- coding: utf-8 -*-

"""
snatch.utils
~~~~~~~~~~~~

Utility functions and filters for snatch

:copyright: (c) 2013 by Richard Maisano.
:license: Apache 2.0, see LICENSE for more details.

"""

def extension_filter_maker(extension_set):
    """Dynamically creates an extension filter

    :param extension_set: lits of acceptable extensions to filter by
    :type extension_set: tuple, list

    :return: function that filters by image extension
    """

    extension_set = map(str.lower, extension_set)

    def extension_filter(images):
        def match_extension(image):
            return image.extension in extension_set
        return filter(match_extension, images)

    return extension_filter
