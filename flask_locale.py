# -*- coding: utf-8 -*-
"""
Flask-Locale
----


Modified from Tornado.Locale and Flask-Babel
"""

import os
import re
import csv
from flask import _request_ctx_stack


__all__ = ('Locale', 'refresh', 'translate')


def get_app():
    ctx = _request_ctx_stack.top
    if not ctx:
        return None
    return ctx.app


def to_unicode(value):
    """Converts a string argument to a unicode string.

    If the argument is already a unicode string or None, it is returned
    unchanged.  Otherwise it must be a byte string and is decoded as utf8.
    """
    if isinstance(value, unicode):
        return value
    assert isinstance(value, bytes)
    return value.decode("utf-8")


def load_translations(directory):
    u"""Loads translations from CSV files in a directory.

    Translations are strings with optional Python-style named placeholders
    (e.g., "My name is %(name)s") and their associated translations.

    The directory should have translation files of the form LOCALE.csv,
    e.g. es_GT.csv. The CSV files should have two or three columns: string,
    translation, and an optional plural indicator. Plural indicators should
    be one of "plural" or "singular". A given string can have both singular
    and plural forms. For example "%(name)s liked this" may have a
    different verb conjugation depending on whether %(name)s is one
    name or a list of names. There should be two rows in the CSV file for
    that string, one with plural indicator "singular", and one "plural".
    For strings with no verbs that would change on translation, simply
    use "unknown" or the empty string (or don't include the column at all).

    The file is read using the csv module in the default "excel" dialect.
    In this format there should not be spaces after the commas.

    Example translation es_LA.csv:

        "I love you","Te amo"
        "%(name)s liked this","A %(name)s les gust\u00f3 esto","plural"
        "%(name)s liked this","A %(name)s le gust\u00f3 esto","singular"
    """
    _translations = {}
    for path in os.listdir(directory):
        if not path.endswith(".csv"):
            continue
        locale, extension = path.split(".")
        if not re.match("[a-z]+(_[A-Z]+)?$", locale):
            continue
        full_path = os.path.join(directory, path)
        try:
            # python 3: csv.reader requires a file open in text mode.
            # Force utf8 to avoid dependence on $LANG environment variable.
            f = open(full_path, "r", encoding="utf-8")
        except TypeError:
            # python 2: files return byte strings, which are decoded below.
            # Once we drop python 2.5, this could use io.open instead
            # on both 2 and 3.
            f = open(full_path, "r")
        _translations[locale] = {}
        for row in csv.reader(f):
            if not row or len(row) < 2:
                continue
            row = [to_unicode(c).strip() for c in row]
            english, translation = row[:2]
            if len(row) > 2:
                plural = row[2] or "unknown"
            else:
                plural = "unknown"
            if plural not in ("plural", "singular", "unknown"):
                continue
            _translations[locale].setdefault(plural, {})[english] = translation
        f.close()
    return _translations


class Locale(object):
    """Central controller class that can be used to configure how
    Flask-Locale behaves.  Each application that wants to use Flask-Locale
    has to create, or run :meth:`init_app` on, an instance of this class
    after the configuration was initialized.
    """

    def __init__(self, app=None, default_locale='en', configure_jinja=True):
        self._default_locale = default_locale
        self._configure_jinja = configure_jinja

        if app:
            self.init_app(app)

    def init_app(self, app):
        """Set up this instance for use with *app*, if no app was passed to
        the constructor.
        """
        self.app = app
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['locale'] = self

        app.config.setdefault('DEFAULT_LOCALE', self._default_locale)
        locale_path = os.path.join(app.root_path, 'translations')
        app.config.setdefault('LOCALE_PATH', locale_path)

        if self._configure_jinja:
            app.jinja_env.add_extension('jinja2.ext.i18n')
            app.jinja_env.install_gettext_callables(
                translate,
                translate,
                newstyle=True
            )

    def localeselector(self, f):
        """Registers a callback function for locale selection.  The default
        behaves as if a function was registered that returns `None` all the
        time.  If `None` is returned, the locale falls back to the one from
        the configuration.

        This has to return the locale as string (eg: ``'de_AT'``, ''`en_US`'')
        """
        assert not hasattr(self, 'locale_selector_func'), \
            'a localeselector function is already registered'
        self.locale_selector_func = f
        return f


def get_translations():
    """Returns the correct gettext translations that should be used for
    this request.  This will never fail and return a dummy translation
    object if used outside of the request or if a translation cannot be
    found.
    """
    app = get_app()
    translations = getattr(app, 'locale_translations', None)
    if not translations:
        dirname = app.config['LOCALE_PATH']
        translations = load_translations(dirname)
        app.locale_translations = translations
    return translations


def get_locale():
    """Returns the locale that should be used for this request as
    `locale.Locale` object.  This returns `None` if used outside of
    a request.
    """
    app = get_app()
    locale = getattr(app, 'current_locale', None)
    if not locale:
        locale_instance = app.extensions['locale']
        locale = app.config['DEFAULT_LOCALE']
        if hasattr(locale_instance, 'locale_selector_func'):
            rv = locale.locale_selector_func()
            if rv:
                locale = rv
        app.current_locale = locale
    return locale


def refresh():
    """Refreshes the cached timezones and locale information.  This can
    be used to switch a translation between a request and if you want
    the changes to take place immediately, not just with the next request::

        user.locale = request.form['locale']
        refresh()
        flash(gettext('Language was changed'))

    Without that refresh, the :func:`~flask.flash` function would probably
    return English text and a now German page.
    """
    ctx = _request_ctx_stack.top
    if not ctx:
        return None
    if hasattr(ctx, 'current_locale'):
        delattr(ctx, 'current_locale')

    app = ctx.app
    if hasattr(app, 'locale_translations'):
        delattr(app, 'locale_translations')


def translate(message, plural_message=None, count=None):
    translations = get_translations()
    current_locale = get_locale()
    translation_locale = translations[current_locale]
    if plural_message:
        assert count
        if count != 1:
            message = plural_message
            message_dict = translation_locale.get("plural", {})
        else:
            message_dict = translation_locale.get("singular", {})
    else:
        message_dict = translation_locale.get("unknown", {})
    return message_dict.get(message, message)
