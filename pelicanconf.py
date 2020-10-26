#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = "Joseph (Sephi) Berry"
SITENAME = "Geo Berry"
SITEURL = ""

PATH = "content"

TIMEZONE = "Asia/Jerusalem"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = 10

MARKUP = ("md", "ipynb")

from pelican_jupyter import markup as nb_markup

IGNORE_FILES = [".ipynb_checkpoints"]

THEME = "themes/brutalist/brutalist"
# THEME = "themes/pelican-blue/pelican-blue"
# PLUGINS
PLUGIN_PATHS = ["plugins", "plugins/ibynb", "plugins/pelican-plugins"]
PLUGINS = [
    nb_markup,
    "sitemap",
    # "category_order",
    # "w3c_validate",
    "optimize_images",
    "gzip_cache",
]

## SITEMAP PLUGIN
SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.99, "pages": 0.75, "indexes": 0.5},
    "changefreqs": {"articles": "daily", "pages": "daily", "indexes": "daily"},
}
# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
