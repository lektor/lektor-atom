# -*- coding: utf-8 -*-
import sys
import hashlib
import uuid
from datetime import datetime, date

import click
import pkg_resources
from lektor.build_programs import BuildProgram
from lektor.db import F
from lektor.environment import Expression, FormatExpression
from lektor.pluginsystem import Plugin
from lektor.context import get_ctx, url_to
from lektor.sourceobj import VirtualSourceObject
from lektor.utils import build_url

from werkzeug.contrib.atom import AtomFeed
from markupsafe import escape

PY2 = sys.version_info[0] == 2

if PY2:
    text_type = unicode
else:
    text_type = str


class AtomFeedSource(VirtualSourceObject):
    def __init__(self, parent, feed_id, plugin):
        VirtualSourceObject.__init__(self, parent)
        self.plugin = plugin
        self.feed_id = feed_id

    @property
    def path(self):
        return self.parent.path + '@atom/' + self.feed_id

    @property
    def url_path(self):
        p = self.plugin.get_atom_config(self.feed_id, 'url_path',
                                        alt=self.alt)
        if p:
            cfg = self.plugin.env.load_config()
            primary_alts = '_primary', cfg.primary_alternative
            if self.alt not in primary_alts:
                p = "/%s%s" % (self.alt, p)
            return p

        return build_url([self.parent.url_path, self.filename])

    def __getattr__(self, item):
        try:
            return self.plugin.get_atom_config(self.feed_id, item,
                                               alt=self.alt)
        except KeyError:
            raise AttributeError(item)

    @property
    def feed_name(self):
        return self.plugin.get_atom_config(self.feed_id, 'name', alt=self.alt) \
            or self.feed_id


def get(item, field, default=None):
    if field in item:
        return item[field]
    return default


def get_id(s):
    b = hashlib.md5(s.encode('utf-8')).digest()
    return uuid.UUID(bytes=b, version=3).urn


def get_item_title(item, field):
    if field in item:
        return item[field]
    return item.record_label


def get_item_updated(item, field):
    if field in item:
        rv = item[field]
    else:
        rv = datetime.utcnow()
    if isinstance(rv, date) and not isinstance(rv, datetime):
        rv = datetime(*rv.timetuple()[:3])
    return rv


class AtomFeedBuilderProgram(BuildProgram):
    def format_expression(self, expression, record, env):
        with get_ctx().changed_base_url(record.url_path):
            return FormatExpression(env, expression).evaluate(
                record.pad,
                this=record,
                alt=record.alt
            )

    def produce_artifacts(self):
        self.declare_artifact(
            self.source.url_path,
            sources=list(self.source.iter_source_filenames()))

    def build_artifact(self, artifact):
        ctx = get_ctx()
        feed_source = self.source
        blog = feed_source.parent

        summary = self.format_expression(
            feed_source.blog_summary,
            blog,
            ctx.env)

        blog_author = self.format_expression(
            feed_source.blog_author,
            blog,
            ctx.env
        )

        generator = ('Lektor Atom Plugin',
                     'https://github.com/ajdavis/lektor-atom',
                     pkg_resources.get_distribution('lektor-atom').version)

        feed = AtomFeed(
            title=feed_source.feed_name,
            subtitle=summary,
            subtitle_type='html', 
            author=blog_author,
            feed_url=url_to(feed_source, external=True, alt=feed_source.alt),
            url=url_to(blog, external=True, alt=feed_source.alt),
            id=get_id(ctx.env.project.id),
            generator=generator)

        if feed_source.items:
            # "feed_source.items" is a string like "site.query('/blog')".
            expr = Expression(ctx.env, feed_source.items)
            items = expr.evaluate(ctx.pad)
        else:
            items = blog.children

        # Don’t force the user to think about alt when specifying an items
        # query.
        items.alt = feed_source.alt

        if feed_source.item_model:
            items = items.filter(F._model == feed_source.item_model)

        order_by = '-' + feed_source.item_date_field
        items = items.order_by(order_by).limit(int(feed_source.limit))

        for item in items:
            try:
                item_author = self.format_expression(
                    feed_source.item_author,
                    item,
                    ctx.env
                ) or blog_author
                # FIXME Work-around Lektor #583. When the item is an attachment,
                # we will get an invalid path here unless we force the
                # `_primary` alt.
                url = (
                    item.url_to(item.path, external=True, alt='_primary')
                    if item.is_attachment
                    else url_to(item, external=True)
                )
                base_url = url_to(
                    item.parent if item.is_attachment else item,
                    external=True
                )
                body = self.format_expression(
                    feed_source.item_body,
                    item,
                    ctx.env
                )
                title = self.format_expression(
                    feed_source.item_title,
                    item,
                    ctx.env
                )
                feed.add(
                    title,
                    body,
                    xml_base=base_url,
                    url=url,
                    content_type='html',
                    id=get_id(u'%s/%s' % (
                        ctx.env.project.id,
                        item['_path'].encode('utf-8'))),
                    author=item_author,
                    updated=get_item_updated(item, feed_source.item_date_field))
            except Exception as exc:
                msg = '%s: %s' % (item['_id'], exc)
                click.echo(click.style('E', fg='red') + ' ' + msg)

        with artifact.open('wb') as f:
            f.write(feed.to_string().encode('utf-8'))


class AtomPlugin(Plugin):
    name = u'Lektor Atom plugin'
    description = u'Lektor plugin that generates Atom feeds.'

    defaults = {
        'source_path': '/',
        'name': None,
        'url_path': None,
        'filename': 'feed.xml',
        'blog_author': '{{ this.author }}',
        'blog_summary': '{{ this.summary }}',
        'items': None,
        'limit': 50,
        'item_title': '{{ this.title or this.record_label }}',
        'item_body': '{{ this.body }}',
        'item_author': '{{ this.author }}',
        'item_date_field': 'pub_date',
        'item_model': None,
    }

    def get_atom_config(self, feed_id, key, alt=None):
        default_value = self.defaults[key]
        config = self.get_config()
        primary_value = config.get(
            "%s.%s" % (feed_id, key),
            default_value
        )
        localized_value = (
            config.get("%s.%s.%s" % (feed_id, alt, key))
            if alt
            else None
        )
        return localized_value or primary_value

    def on_setup_env(self, **extra):
        self.env.add_build_program(AtomFeedSource, AtomFeedBuilderProgram)

        self.env.jinja_env.filters['atom_feeds'] = self.atom_feeds
        self.env.jinja_env.globals['atom_feeds'] = self.atom_feeds

        @self.env.virtualpathresolver('atom')
        def feed_path_resolver(node, pieces):
            if len(pieces) != 1:
                return

            _id = pieces[0]

            if _id not in self._feed_ids():
                return

            source_path = self.get_atom_config(_id, 'source_path',
                                               alt=node.alt)
            if node.path == source_path:
                return AtomFeedSource(node, _id, plugin=self)

        @self.env.generator
        def generate_feeds(source):
            for _id in self._feed_ids():
                if source.path == self.get_atom_config(_id, 'source_path',
                                                       alt=source.alt):
                    yield AtomFeedSource(source, _id, self)

    def _feed_ids(self):
        feed_ids = set()
        for section in self.get_config().sections():
            if '.' in section:
                feed_id, _alt = section.split(".")
            else:
                feed_id = section
            feed_ids.add(feed_id)

        return feed_ids

    def _all_feeds(self, alt=None):
        ctx = get_ctx()

        feeds = []
        for feed_id in self._feed_ids():
            path = self.get_atom_config(feed_id, 'source_path', alt=alt)
            feed = ctx.pad.get(
                '%s@atom/%s' % (path, feed_id),
                alt=alt or ctx.record.alt
            )
            if feed:
                feeds.append(feed)

        return feeds

    def _feeds_for(self, page, alt=None):
        ctx = get_ctx()
        record = page.record

        feeds = []
        for section in self._feed_ids():
            feed = ctx.pad.get(
                '%s@atom/%s' % (record.path, section),
                alt=alt or ctx.record.alt
            )
            if feed:
                feeds.append(feed)

        return feeds

    def atom_feeds(self, for_page=None, alt=None):
        if not for_page:
            return self._all_feeds(alt=alt)
        else:
            return self._feeds_for(for_page, alt=alt)
