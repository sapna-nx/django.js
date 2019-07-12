from django.test import TestCase

from djangojs.utils import StorageGlobber

from os.path import normpath


class StorageGlobberTest(TestCase):
    def test_no_js_file(self):
        '''Should handle empty js file list'''
        self.assertEqual(StorageGlobber.glob(), [])

    def test_single_js_file(self):
        '''Should handle a single js file name as string'''
        files = 'test/libs/jasmine-djangojs.js'
        expected = [normpath('test/libs/jasmine-djangojs.js')]
        self.assertEqual(StorageGlobber.glob(files), expected)

    def test_multi_js_file(self):
        '''Should handle an array of js file names'''
        files = ['test/libs/jasmine-djangojs.js', 'test/libs/jasmine.js']
        result = StorageGlobber.glob(files)

        self.assertIn(normpath('test/libs/jasmine-djangojs.js'), result)
        self.assertIn(normpath('test/libs/jasmine.js'), result)

    def test_single_glob_expression(self):
        '''Should handle a single glob pattern as js file list'''
        files = 'test/libs/jasmine-*.js'
        result = StorageGlobber.glob(files)

        self.assertIn(normpath('test/libs/jasmine-djangojs.js'), result)
        self.assertIn(normpath('test/libs/jasmine-html.js'), result)
        self.assertIn(normpath('test/libs/jasmine-jquery.js'), result)
        self.assertNotIn(normpath('test/libs/jasmine.js'), result)

    def test_multi_glob_expression(self):
        '''Should handle a glob pattern list as js file list'''
        files = ['test/libs/jasmine-*.js', 'test/libs/qunit-*.js']
        result = StorageGlobber.glob(files)

        self.assertIn(normpath('test/libs/jasmine-djangojs.js'), result)
        self.assertIn(normpath('test/libs/jasmine-html.js'), result)
        self.assertIn(normpath('test/libs/jasmine-jquery.js'), result)
        self.assertIn(normpath('test/libs/qunit-tap.js'), result)
        self.assertNotIn(normpath('test/libs/jasmine.js'), result)
        self.assertNotIn(normpath('test/libs/qunit.js'), result)

    def test_preserve_order(self):
        '''Should preserve declaration order'''
        # Orders matters: should not be an alphabeticaly sorted list
        files = ['test/libs/jasmine.js', 'djangojs/django.js', 'test/libs/qunit-*.js']
        result = StorageGlobber.glob(files)

        self.assertEqual(result[0], normpath('test/libs/jasmine.js'))
        self.assertEqual(result[1], normpath('djangojs/django.js'))

        for lib in result[2:]:
            self.assertIn(normpath('test/libs/qunit-'), lib)
            self.assertTrue(lib.endswith('.js'))
