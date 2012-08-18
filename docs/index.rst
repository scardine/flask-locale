.. Flask-Locale documentation master file, created by
   sphinx-quickstart on Sat Aug 18 10:48:19 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Flask-Locale
==============

.. module:: flask.ext.locale

Flask-Locale is an extension to `Flask <http://flask.pocoo.org/>`_ that adds i18n and l10n support to
any Flask application.

Installation
------------

Install the extension with one of the following commands::

    $ easy_install Flask-Locale

or alternatively if you have pip installed::

    $ pip install Flask-Locale

Please note that Flask-Locale requires Jinja 2.5.  If you are using an
older version you will have to upgrade or disable the Jinja support.

Configuration
-------------

To get started all you need to do is to instanciate a :class:`Locale`
object after configuring the application::

    from flask import Flask
    from flask.ext.locale import Locale, translate

    app = Flask(__name__)
    app.config.from_pyfile('mysettings.cfg')
    locale = Locale(app)

The locale object itself can be used to configure the locale support
further.  Locale has two configuration values that can be used to change
some internal defaults:

=========================== =============================================
`DEFAULT_LOCALE`            The default locale to use if no locale
                            selector is registered.  This defaults
                            to ``'en'``.
`LOCALE_PATH`               The path to translation files.  
                            This defaults to ``'./translations'``
=========================== =============================================

For more complex applications you might want to have multiple applications
for different users which is where selector functions come in handy.  The
first time the locale extension needs the locale (language code) of the
current user it will call a :meth:`~Locale.localeselector` function.

If `localeselector` return `None` the extension will automatically
fall back to the user’s locale from Accept-Language header(:meth:`~Locale.get_browser_locale`).If the extension 
can't find the translation for the user's locale, it will fall back to `DEFAULT_LOCALE`.

Translations are loaded only once and then cached.  If you
need to reload the translations, you can :func:`refresh` the
cache.

Example selector functions:: code-block:: python

    from flask import g, request

    @locale.localeselector
    def get_locale():
        # if a user is logged in, use the locale from the user settings
        user = getattr(g, 'user', None)
        if user is not None:
            return user.locale
        # otherwise return None and the extension will automatically
        # fall back to the user’s locale from Accept-Language header.
        return None


The example above assumes that the current user is stored on the
:data:`flask.g` object.

Using Translations
-------------------

:func:`trnaslate` is responsible for translating.

Here are examples:  

.. code-block:: python

   from flask.ext.locale import translate

   translate('String')
   translate('I'm %s years old.') % age
   translate('%s Apple', '%s Apples', number_of_apples) % number_of_apples

To create translation files,look at the doc of :meth:`~Locale.load_translations`

API
---

This part of the documentation documents each and every public class or
function from Flask-Babel.

Configuration
`````````````

.. autoclass:: Locale
   :members:

Context Functions
`````````````````

.. autofunction:: translate

Low-Level API
`````````````

.. autofunction:: refresh