SITENAME = 'pelican_domain_annotations test'
SITEURL = 'http://localhost:8000'

TIMEZONE = 'Europe/Rome'
DEFAULT_LANG = 'en'
DEFAULT_PAGINATION = False
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

RELATIVE_URLS = True

PATH = "content"
OUTPUT_PATH = "build"

STATIC_PATHS = []

PLUGIN_PATHS = [
    "../pelican/plugins",
]

PLUGINS = [
    "domain_annotations",
]
