import os
import shutil
import tempfile
from datetime import datetime

import pytest
from lektor.types import Type


class DatetimeType(Type):
    def value_from_raw(self, raw):
        return datetime.strptime(raw.value, "%Y-%m-%d %H:%M:%S")


@pytest.fixture(scope="function")
def project(request):
    from lektor.project import Project

    return Project.from_path(os.path.join(os.path.dirname(__file__), "demo-project"))


@pytest.fixture(scope="function")
def env(request, project):
    from lektor.environment import Environment

    e = Environment(project)
    e.types["datetime"] = DatetimeType  # As if we had a datetime plugin.
    return e


@pytest.fixture(scope="function")
def pad(request, env):
    from lektor.db import Database

    return Database(env).new_pad()


def make_builder(request, pad):
    from lektor.builder import Builder

    out = tempfile.mkdtemp()
    b = Builder(pad, out)

    def cleanup():
        try:
            shutil.rmtree(out)
        except (OSError, IOError):
            pass

    request.addfinalizer(cleanup)
    return b


@pytest.fixture(scope="function")
def builder(request, pad):
    return make_builder(request, pad)


@pytest.fixture(scope="function")
def F():
    from lektor.db import F

    return F


@pytest.fixture(scope="function")
def reporter(request, env):
    from lektor.reporter import BufferReporter

    r = BufferReporter(env)
    r.push()
    request.addfinalizer(r.pop)
    return r
