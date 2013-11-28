import os
import sys

# ugly sys.path hack for testing:
DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = DIR.rsplit('/', 1)[0]
sys.path.insert(0, PARENT_DIR)

import unittest

from threading import Thread
from SocketServer import TCPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

from snatch import snatch


class TestSnatch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        port = 8000
        base = 'http://localhost:%s/test/static' % (port)
        cls.URLS = {
            'two gifs': '%s/two-gifs.html' % (base),
            'one jpg, one gif, one png': '%s/jpg-gif-png.html' % (base),
            'one gif, four pngs': '%s/one-gif-four-pngs.html' % (base),
            'has base tag': '%s/has-base-tag.html' % (base),
            'explicit dimensions': '%s/explicit-dimensions.html' % (base),
            'srcless': '%s/srcless.html' % (base)
        }
        cls.httpd = TCPServer(('', port), SimpleHTTPRequestHandler)
        t = Thread(target=cls.httpd.serve_forever)
        t.setDaemon(True)
        t.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()

    def test_extensions(self):
        images = snatch(self.URLS['two gifs'])
        self.assertEqual(images.extensions, ['gif'])

        images = snatch(self.URLS['one jpg, one gif, one png'])
        self.assertEqual(images.extensions, ['jpg', 'gif', 'png'])

        images = snatch(self.URLS['one gif, four pngs'])
        self.assertEqual(images.extensions, ['gif', 'png'])

    def test_base_tag(self):
        images = snatch(self.URLS['has base tag'])
        self.assertTrue(images[0].url.startswith('http://foo.bar'))

    def test_explicit_dimensions(self):
        images = snatch(self.URLS['explicit dimensions'])
        self.assertEqual(images[0].width, 200)
        self.assertEqual(images[0].height, 100)

    def test_duplicate_images(self):
        images = snatch(self.URLS['one gif, four pngs'])
        self.assertEqual(len(images), 3)
        self.assertEqual(images[2].count, 3)
        self.assertEqual(sum(i.count for i in images), 5)

    def test_hooks(self):
        self.value = False
        def callback(images):
            self.value = True
        callbacks = {'complete': callback}
        self.assertEqual(self.value, False)
        images = snatch(self.URLS['two gifs'], callbacks=callbacks)
        self.assertEqual(self.value, True)

    def test_multiple_hooks(self):
        self.value = 'a'
        def callback1(images):
            self.value += 'b'
        def callback2(images):
            self.value += 'c'
        callbacks = {'complete': [callback1, callback2]}
        images = snatch(self.URLS['two gifs'], callbacks=callbacks)
        self.assertEqual(self.value, 'abc')

    def test_filtering_with_hooks(self):
        images = snatch(self.URLS['explicit dimensions'])
        self.assertEqual(len(images), 2)

        def wider_than_200(images):
            def filter_fn(image):
                return image.width > 200
            return filter(filter_fn, images)

        callbacks = {'complete': wider_than_200}
        images = snatch(self.URLS['explicit dimensions'], callbacks=callbacks)
        self.assertEqual(len(images), 1)
        self.assertTrue(images[0].width > 200)

    def test_filterting_by_extension(self):
        images = snatch(self.URLS['one jpg, one gif, one png'],
            with_extension=('gif',))
        self.assertEqual(images.extensions, ['gif'])

        images = snatch(self.URLS['one jpg, one gif, one png'])
        self.assertEqual(images.extensions, ['jpg', 'gif', 'png'])

        images = images.with_extension('png')
        self.assertEqual(images.extensions, ['png'])

    def test_srcless(self):
        images = snatch(self.URLS['srcless'])
        self.assertEqual(len(images), 1)


if __name__ == '__main__':
    unittest.main()
