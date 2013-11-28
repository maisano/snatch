Snatch: Simple Image Scraping in Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configurable, extensible image scraping for Python. Inspired by the design and internals of Kenneth Reitz' `Requests <https://github.com/kennethreitz/requests>`_ library.

.. code-block:: python

    >>> from snatch import snatch
    >>> images = snatch('http://octodex.github.com/pythocat/')
    >>> images.extensions
    [u'png']
    >>> images[1]
    <Image ["pythocat.png"]>
    >>> images[1].url
    u'http://octodex.github.com/images/pythocat.png'

Easily usable, easily configurable:

.. code-block:: python

    >>> url = 'url/with/54/images'
    >>> snatch(url)
    <ImageList [54]>

    # reduce your results by extension:
    >>> _.with_extension('gif')
    <ImageList [2]>

    # or more explicitly limit your extension in the inital api call:
    >>> snatch(url, with_extension=('gif',))
    <ImageList [2]>

It's also very easy to hook your own filters or operations into Snatch's callbacks system. Let's say you only wanted to capture images that were larger than 250 px wide:

.. code-block:: python

    import requests
    import Image
    from StringIO import StringIO
    from snatch import snatch

    def wider_than_250(images):
        def filter_fn(image):
            if image.width is None:
                res = requests.get(image.src)
                img = Image.open(StringIO(res.content))
                image.width = img.size[0]
            return image.width > 250
        return filter(filter_fn, images)

    url = 'http://octodex.github.com/images/pythocat.png'
    callbacks = {'complete': wider_than_250}
    images = snatch(url, callbacks=callbacks)


And even simpler to download all images from a URL:

.. code-block:: python

    import os
    import requests
    from snatch import snatch

    directory = 'snatched-images'

    if not os.path.exists(directory):
        os.mkdir(directory)

    for image in snatch('http://octodex.github.com/pythocat/'):
        contents = requests.get(image.url).content
        with open('%s/%s' % (directory, image.filename), 'w') as image_file:
            image_file.write(contents)
