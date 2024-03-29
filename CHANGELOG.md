# Changelog

## 0.4.0 (September 17, 2021)

- Replace Werkzeug's
  [Atom](https://werkzeug.palletsprojects.com/en/0.15.x/contrib/atom/)
  with Pelican's Django-based
  [feedgenerator](https://github.com/getpelican/feedgenerator)
- Fix [#10][] whereby atom feed pages were being auto-pruned in some cases when alternatives (i18n) were in use. (PR [#35][])

[#10]: <https://github.com/lektor/lektor-atom/issues/10>
[#35]: <https://github.com/lektor/lektor-atom/pull/35>

## 0.3.1 (May 11, 2020)

- Pin werkzeug to be able to use the atom feed.

## 0.3 (May 18, 2019)

- Ensure universal builds
- Bugfix in build program
- Better README

## Version 0.2 (February 2, 2016)

- Python 3 compatibility (thanks to Dan Bauman).
- colored error output during build, fix for Markdown-formatted item subtitles.

## Version 0.1 (September 1, 2016)

- Initial release.
