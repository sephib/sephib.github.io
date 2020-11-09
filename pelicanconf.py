#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = "Joseph (Sephi) Berry"
SITENAME = "Geo Berry"
SITEURL = ""  #"http://localhost:8000"
SITETITLE = "Sephi's Blog"
SITESUBTITLE = "Project Manager | Data Engineer | Geo-Spatial Specialist"
SITEDESCRIPTION = "Sephi's Thoughts and Writings"
SITELOGO = SITEURL + "/images/avatar_osnx.png"
FAVICON = SITEURL + "/images/favicon.ico"


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
# LINKS = (
#     ("Pelican", "https://getpelican.com/"),
#     ("Python.org", "https://www.python.org/"),
#     ("Jinja2", "https://palletsprojects.com/p/jinja/"),
#     ("You can modify those links in your config file", "#"),
# )

# Social widget
SOCIAL = (('linkedin', 'https://www.linkedin.com/in/berrygis'),
          ('github', 'https://github.com/sephib'),
          ('twitter', 'https://twitter.com/geosephi'),
        #   ('stack-overflow', 'http://stackoverflow.com/story/girisagar46.github.io'),
          )

DEFAULT_PAGINATION = 10

MARKUP = ("md", "ipynb")

from pelican_jupyter import markup as nb_markup

IGNORE_FILES = [".ipynb_checkpoints"]


THEME = "themes/Flex"
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
