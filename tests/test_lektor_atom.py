import os

from lxml import objectify


def test_typical_feed(pad, builder):
    failures = builder.build_all()
    assert not failures
    feed_path = os.path.join(builder.destination_path, 'typical-blog/feed.xml')
    feed = objectify.parse(open(feed_path)).getroot()
    
    assert 'Feed One' == feed.title
    assert 'My Summary' == feed.subtitle
    assert 'text' == feed.subtitle.attrib['type']
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


def test_virtual_resolver(pad, builder):
    feed = pad.get('typical-blog@feed.xml')
    assert feed and feed.feed_name == 'Feed One'
    url_path = pad.get('typical-blog/post1').url_to(feed)
    assert url_path == '../../typical-blog/feed.xml'

    feed = pad.get('typical-blog2@feed.xml')
    assert feed and feed.feed_name == 'Feed Two'

    feed = pad.get('custom-blog@atom.xml')
    assert feed and feed.feed_name == 'Feed Three'
    url_path = pad.get('custom-blog/post1').url_to(feed)
    assert url_path == '../../custom-blog/atom.xml'
