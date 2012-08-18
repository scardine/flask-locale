# -*- coding: utf-8 -*-
from __future__ import with_statement

import unittest
from flask import Flask
from flask.ext.locale import Locale, translate, to_unicode


class LocaleTestCase(unittest.TestCase):

    def test_basic(self):
        app = Flask(__name__)
        Locale(app)

        with app.test_request_context():
            assert translate('hello') == 'hello'
            assert translate('a', 'b', 1) == 'a'
            assert translate('a', 'b', 2) == 'b'

    def test_translate(self):
        app = Flask(__name__)
        app.config['DEFAULT_LOCALE'] = 'zh_CN'
        Locale(app)

        with app.test_request_context():
            assert translate('I love you') == to_unicode('我爱你')

    def test_custom_locale_selector(self):
        app = Flask(__name__)
        l = Locale(app)

        the_locale = 'zh_CN'

        @l.localeselector
        def select_locale():
            return the_locale

        with app.test_request_context():
            assert translate('I love you') == to_unicode('我爱你')

        the_locale = 'en'
        with app.test_request_context():
            assert translate('I love you') == to_unicode('I love you')

        the_locale = 'es_LA'
        with app.test_request_context():
            assert translate('I love you') == to_unicode('Te amo')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LocaleTestCase))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
