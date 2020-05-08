import ast
import io
import re

from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

_description_re = re.compile(r"description\s+=\s+(?P<description>.*)")

with open("lektor_atom.py", "rb") as f:
    description = str(
        ast.literal_eval(_description_re.search(f.read().decode("utf-8")).group(1))
    )

tests_require = (["lxml", "pytest"],)


setup(
    author=u"A. Jesse Jiryu Davis",
    author_email="jesse@emptysquare.net",
    description=description,
    install_requires=[
        "MarkupSafe",
        "Werkzeug<1.0",  # Werkzeug 1.0 removed the feed generator
    ],
    keywords="Lektor plugin static-site blog atom rss",
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    name="lektor-atom",
    py_modules=["lektor_atom"],
    url="https://github.com/nixjdm/lektor-atom",
    version="0.3.1",
    classifiers=[
        "Environment :: Plugins",
        "Environment :: Web Environment",
        "Framework :: Lektor",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"lektor.plugins": ["atom = lektor_atom:AtomPlugin"]},
    extras_require={"test": tests_require},
    tests_require=tests_require,
)
