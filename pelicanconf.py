AUTHOR = 'Stanislav Pankevich'
SITENAME = "TECH NOTES"
SITESUBTITLE = " by Stanislav Pankevich"
SITEURL = 'https://stanislaw.github.io'

PATH = 'content'

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('StrictDoc project (requirements management)', 'https://github.com/strictdoc-project/strictdoc'),
         ('Mull project (mutation testing)', 'https://github.com/mull-project/mull'),
         ('awesome-safety-critical (reading list)', 'https://github.com/stanislaw/awesome-safety-critical'),
        )

# Social widget
SOCIAL = (
          ('stanislaw', 'https://github.com/stanislaw'),
          ('stanislav-pankevich', 'https://stackoverflow.com/users/598057/stanislav-pankevich'),
          ('stanislavpankevich', 'https://www.linkedin.com/in/stanislavpankevich'),
        )

DEFAULT_PAGINATION = False

# THEME = "themes/simple"
THEME = "themes/mottto"

STATIC_PATHS = ['images', 'files']

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["pelican-toc"]

TOC = {
    'TOC_INCLUDE_TITLE': 'false',  # If 'true' include title in toc
}

# Uncomment following line if you want to show the 'Fork me on Github' strip
# GITHUB_URL = ''

# Uncomment following line if you want to show the tweet button under the article title
TWITTER_USERNAME = 'sbpankevich'

# Uncomment following line if you want to enable comments
# DISQUS_SITENAME = ''
GOOGLE_ANALYTICS = True
