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


setup(
    author=u"A. Jesse Jiryu Davis",
    author_email="jesse@emptysquare.net",
    description=description,
    install_requires=["MarkupSafe", "feedgenerator"],
    keywords="Lektor plugin static-site blog atom rss",
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    name="lektor-atom",
    py_modules=["lektor_atom"],
    url="https://github.com/lektor/lektor-atom",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    classifiers=[
        "Environment :: Plugins",
        "Environment :: Web Environment",
        "Framework :: Lektor",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"lektor.plugins": ["atom = lektor_atom:AtomPlugin"]},
)
