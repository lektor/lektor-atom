# -*- coding: utf-8 -*-

import os

from lektor.context import Context
from lxml import objectify


def test_typical_feed(pad, builder):
    failures = builder.build_all()
    assert not failures
    feed_path = os.path.join(builder.destination_path, 'typical-blog/feed.xml')
    feed = objectify.parse(open(feed_path)).getroot()
    
    assert 'Feed One' == feed.title
    assert 'My Summary' == feed.subtitle
    assert 'html' == feed.subtitle.attrib['type']
    assert 'A. Jesse Jiryu Davis' == feed.author.name
    assert 'http://x.com/typical-blog/' == feed.link[0].attrib['href']
    assert 'http://x.com/typical-blog/feed.xml' == feed.link[1].attrib['href']
    assert 'self' == feed.link[1].attrib['rel']
    assert 'Lektor Atom Plugin' == feed.generator

    assert 2 == len(feed.entry)
    post2, post1 = feed.entry      # Most recent first.

    assert 'Post 2' == post2.title
    assert '2015-12-13T00:00:00Z' == post2.updated
    assert '<p>bar</p>' == str(post2.content).strip()
    assert 'html' == post2.content.attrib['type']
    assert 'http://x.com/typical-blog/post2/' == post2.link.attrib['href']
    base = post2.attrib['{http://www.w3.org/XML/1998/namespace}base']
    assert 'http://x.com/typical-blog/post2/' == base
    assert 'Armin Ronacher' == post2.author.name

    assert 'Post 1' == post1.title
    assert '2015-12-12T00:00:00Z' == post1.updated
    assert '<p>foo</p>' == str(post1.content).strip()
    assert 'html' == post1.content.attrib['type']
    assert 'http://x.com/typical-blog/post1/' == post1.link.attrib['href']
    base = post1.attrib['{http://www.w3.org/XML/1998/namespace}base']
    assert 'http://x.com/typical-blog/post1/' == base
    assert 'A. Jesse Jiryu Davis' == post1.author.name


def test_custom_feed(pad, builder):
    failures = builder.build_all()
    assert not failures
    feed_path = os.path.join(builder.destination_path, 'custom-blog/atom.xml')
    feed = objectify.parse(open(feed_path)).getroot()
    
    assert 'Feed Three' == feed.title
    assert '<p>My Description</p>' == str(feed.subtitle).strip()
    assert 'html' == feed.subtitle.attrib['type']
    assert 'A. Jesse Jiryu Davis' == feed.author.name
    assert 'http://x.com/custom-blog/' == feed.link[0].attrib['href']
    assert 'http://x.com/custom-blog/atom.xml' == feed.link[1].attrib['href']
    assert 'self' == feed.link[1].attrib['rel']
    assert 'Lektor Atom Plugin' == feed.generator

    assert 2 == len(feed.entry)
    post2, post1 = feed.entry      # Most recent first.

    assert 'Post 2' == post2.title
    assert '2015-12-13T00:00:00Z' == post2.updated
    assert '<p>bar</p>' == str(post2.content).strip()
    assert 'html' == post2.content.attrib['type']
    assert 'http://x.com/custom-blog/post2/' == post2.link.attrib['href']
    base = post2.attrib['{http://www.w3.org/XML/1998/namespace}base']
    assert 'http://x.com/custom-blog/post2/' == base
    assert 'Armin Ronacher' == post2.author.name

    assert 'Post 1' == post1.title
    assert '2015-12-12T12:34:56Z' == post1.updated
    assert '<p>foo</p>' == str(post1.content).strip()
    assert 'html' == post1.content.attrib['type']
    assert 'http://x.com/custom-blog/post1/' == post1.link.attrib['href']
    base = post1.attrib['{http://www.w3.org/XML/1998/namespace}base']
    assert 'http://x.com/custom-blog/post1/' == base
    assert 'A. Jesse Jiryu Davis' == post1.author.name


def test_multilang_feed(pad, builder):
    failures = builder.build_all()
    assert not failures

    feed_path = os.path.join(builder.destination_path,
                             'de/multilang-blog/feed.xml')
    feed = objectify.parse(open(feed_path)).getroot()

    assert u'Feed Fünf' == feed.title
    assert 'http://x.com/de/multilang-blog/' \
        == feed.link[0].attrib['href']
    assert 'http://x.com/de/multilang-blog/feed.xml' \
        == feed.link[1].attrib['href']
    assert feed.entry.title == 'Post 2 (13.12.2015)'

    base = feed.entry.attrib['{http://www.w3.org/XML/1998/namespace}base']
    assert 'http://x.com/de/multilang-blog/post2/' == base

    feed_path = os.path.join(builder.destination_path,
                             'multilang-blog/feed.xml')
    feed = objectify.parse(open(feed_path)).getroot()

    assert 'Feed Five' == feed.title
    assert 'http://x.com/multilang-blog/' \
        == feed.link[0].attrib['href']
    assert 'http://x.com/multilang-blog/feed.xml' \
        == feed.link[1].attrib['href']
    assert feed.entry.title == 'Post 2 (Dec 13, 2015)'

    base = feed.entry.attrib['{http://www.w3.org/XML/1998/namespace}base']
    assert 'http://x.com/multilang-blog/post2/' == base


def test_virtual_resolver(pad, builder):
    # Pass a virtual source path to url_to().
    feed_path = '/typical-blog@atom/feed-one'
    url_path = pad.get('typical-blog/post1').url_to(feed_path)
    assert url_path == '../../typical-blog/feed.xml'

    # Pass the AtomFeedSource instance itself to url_to().
    feed_instance = pad.get(feed_path)
    assert feed_instance and feed_instance.feed_name == 'Feed One'
    url_path = pad.get('typical-blog/post1').url_to(feed_instance)
    assert url_path == '../../typical-blog/feed.xml'

    feed_instance = pad.get('typical-blog2@atom/feed-two')
    assert feed_instance and feed_instance.feed_name == 'feed-two'

    feed_instance = pad.get('custom-blog@atom/feed-three')
    assert feed_instance and feed_instance.feed_name == 'Feed Three'
    url_path = pad.get('custom-blog/post1').url_to(feed_instance)
    assert url_path == '../../custom-blog/atom.xml'

    feed_instance = pad.get('multilang-blog@atom/feed-five', alt='de')
    assert feed_instance and feed_instance.feed_name == u'Feed Fünf'
    assert feed_instance.url_path == '/de/multilang-blog/feed.xml'


def test_dependencies(pad, builder, reporter):
    reporter.clear()
    builder.build(pad.get('typical-blog@atom/feed-one'))

    assert set(reporter.get_recorded_dependencies()) == set([
        'Website.lektorproject',
        'content/typical-blog',
        'content/typical-blog/contents.lr',
        'content/typical-blog/post1/contents.lr',
        'content/typical-blog/post2/contents.lr',
        'models/blog.ini',
        'models/blog-post.ini',
        'configs/atom.ini',
    ])


def feeds_from_template(pad, template):
    with Context(pad=pad):
        return set(
            pad.env.jinja_env.from_string(template)
                             .render()
                             .split()
        )


def test_discover_all(pad):
    template = r'''
    {% for feed in atom_feeds(alt='_primary') %}
        {{ feed.feed_id }}
    {% endfor %}
    '''
    all_feeds = set(['feed-one', 'feed-two',
                     'feed-three', 'feed-four',
                     'feed-five'])
    feeds_discovered = feeds_from_template(pad, template)
    assert feeds_discovered == all_feeds


def test_discover_local(pad):
    template_blog = r'''
    {% for feed in atom_feeds(for_page=site.get('/custom-blog'), alt='_primary') %}
        {{ feed.feed_id }}
    {% endfor %}
    '''
    feeds_blog = feeds_from_template(pad, template_blog)
    assert feeds_blog == set(['feed-three', 'feed-four'])

    template_noblog = r'''
    {% for feed in atom_feeds(for_page=site.get('/no-feed-content'), alt='_primary') %}
        {{ feed.feed_id }}
    {% endfor %}
    '''
    feeds_noblog = feeds_from_template(pad, template_noblog)
    assert len(feeds_noblog) == 0


def test_localized_config(pad):
    plugin = pad.env.plugins['atom']
    assert plugin.get_atom_config('feed-five', 'name') \
        == 'Feed Five'
    assert plugin.get_atom_config('feed-five', 'name', alt='de') \
        == u'Feed Fünf'

