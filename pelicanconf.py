#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Site settings
AUTHOR = u'mcsrainbow'
AUTHOR_EMAIL = u'guosuiyu@gmail.com'
SITENAME = u'HeyDevOps'
TAGLINE = 'Whatever is worth doing is worth doing well.'
SITEURL = 'http://mcsrainbow.github.io'
DEFAULT_DATE_FORMAT = ('%Y-%m-%d')

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh'
DEFAULT_METADATA = (
)

DELETE_OUTPUT_DIRECTORY = False

# Blogroll
LINKS = (
    ('HeyLinux', 'http://heylinux.com'),
)

# Social widget
SOCIAL = (
    ('Github', 'http://github.com/mcsrainbow/heydevops'),
    ('Twitter', 'http://twitter.com/heydevops'),
)

MENUITEMS = (
)

# Disqus
DISQUS_SITENAME = u"mcsrainbow"

# Content path
PATH = 'content'
PAGE_PATHS = ['pages']
ARTICLE_PATHS = ['articles']
STATIC_PATHS = ['images', 'files']
EXTRA_PATH_METADATA = {
    'files/robots.txt': {'path': 'robots.txt'},
    'images/favicon.ico': {'path': 'favicon.ico'},
}

ARTICLE_URL = ('articles/{slug}.html')
ARTICLE_SAVE_AS = ('articles/{slug}.html')
PAGE_LANG_SAVE_AS = False

# Feed
FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
TRANSLATION_FEED_ATOM = None

# Theme
THEME = 'pelican-themes/zurb-F5-basic'
DEFAULT_PAGINATION = 10

MD_EXTENSIONS = (['codehilite(css_class=highlight)', 'extra',
                  'fenced_code', 'tables', 'sane_lists'])

# Plugin
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = [ 'sitemap', 'gravatar' ]

# Sitemap
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 1,
        'pages': 0.9,
        'indexes': 0.8,
    },
    'changefreqs': {
        'indexes': 'daily',
        'articles': 'daily',
        'pages': 'weekly'
    }
}

# Can be useful in development, but set to False when you're ready to publish
RELATIVE_URLS = False
