from setuptools import setup

setup(
    name='lektor-atom',
    version='0.1',
    author=u'A. Jesse Jiryu Davis',
    author_email='jesse@emptysquare.net',
    license='MIT',
    py_modules=['lektor_atom'],
    install_requires=['MarkupSafe', 'Lektor'],
    entry_points={
        'lektor.plugins': [
            'atom = lektor_atom:AtomPlugin',
        ]
    }
)
