# Lektor Atom Plugin

Builds one or more Atom XML feeds for your [Lektor](https://www.getlektor.com/)-based site.

Inspired by the [atom-feed-support](https://github.com/lektor/lektor-website/tree/master/packages/atom-feed-support) plugin Armin Ronacher wrote for the Lektor official blog.

## Installation

Add lektor-atom to your project from command line:

```
lektor plugins add lektor-atom
```

See [the Lektor documentation for more instructions on installing plugins](https://www.getlektor.com/docs/plugins/).

## Configuration

For each feed you want to publish, add a section to `configs/atom.ini`. For example, a blog with a feed of all recent posts, and a feed of recent posts about coffee:

```
[blog]
name = My Blog
source_path = /
url_path = /feed.xml
items = site.query('/').filter(F.type == 'post')
item_model = blog-post

[coffee]
name = My Blog: Articles About Coffee
source_path = /
url_path = /category/coffee/feed.xml
items = site.query('/blog').filter(F.categories.contains('coffee'))
item_model = blog-post
```

The section names, like `blog` and `coffee`, are just used as internal identifiers.

### Options

| Option            | Default            | Description                                                             |
|-------------------|--------------------|-------------------------------------------------------------------------|
| source\_path      | /                  | Where in the content directory to find items' parent source             |
| name              |                    | Feed name: default is section name                                      |
| filename          | feed.xml           | Name of generated Atom feed file                                        |
| url\_path         |                    | Feed's URL on your site: default is source's URL path plus the filename |
| blog\_author      | {{ this.author }}  | Global blog author or blog editor                                       |
| blog\_summary     | {{ this.summary }} | Blog summary                                                            |
| items             | None               | A query expression: default is the source's children                    |
| limit             | 50                 | How many recent items to include                                        |
| item\_title       | {{ this.title }}   | Blog post title                                                         |
| item\_body        | {{ this.body }}    | Blog post body                                                          |
| item\_author      | {{ this.author }}  | Blog post author                                                        |
| item\_date\_field | pub\_date          | Name of items' publication date field                                   |
| item\_model       | None               | Name of items' model                                                    |

### Customizing the plugin for your models

Use the field options to tell lektor-atom how to read your items. For example, if your site's model is:

```
[model]
name = Blog

[fields.writer]
type = string

[fields.short_description]
type = string
```

Then add to atom.ini:

```
[main]
blog_author = {{ this.writer }}
blog_summary = {{ this.short_description }}
```

See [tests/demo-project/configs/atom.ini](https://github.com/ajdavis/lektor-atom/blob/master/tests/demo-project/configs/atom.ini) for a complete example.

### Filtering items

By default, lektor-atom gets the source at `source_path` and includes all its children in the feed. If you set `item_model`, lektor-atom includes only the children with that data model.

Set `items` to any query expression to override the default. If `items_model` is *also* specified, lektor-atom applies it as a filter to `items`.

## Use In Templates

You can link to a specific feed in your template. If your `atom.ini` contains a feed like this:

```
[main]
source_path = /blog
```

Link to the feed in a template like this:

```
{{ 'blog@atom/main'|url }}
```

The plugin also defines a function to enumerate all feeds or a subset of feeds
relevant to the current page.

```
{% for feed in atom_feeds(for_page=this) %}
    {{ feed | url }}
{% endfor %}
```

When the argument `for_page` is omitted, the function will enumerate all feeds
defined in your project.

## Alternatives

If your site is using Lektor’s alternative system, you can set
alternative-specific configuration values in your `configs/atom.ini`:

```
[blog]
name = My Blog
source_path = /
item_model = blog-post

[blog.de]
name = Mein Blog
```

When lektor-atom is trying to retrieve a configuration value, it will first
look-up the config file section `[feed.ALT]`, where `ALT` is replaced by the
name of the alternative that is being generated. When such a value does not
exist, lektor-atom will get the value from the global section (`[feed]`), or, if
this does not succeed, lektor-atom will fall back on the hardcoded default.

If you are using pybabel and have the Jinja i18n extension enabled, you can
alternatively localize your feeds by using `{% trans %}` blocks inside template
expressions in your `atom.ini`. To extract translation strings using babel, just
add the following to your `babel.cfg`:

```
[jinja2: site/configs/atom.ini]
encoding=utf-8
silent=False
```

# Changes

2016-06-02: Version 0.2. Python 3 compatibility (thanks to Dan Bauman),
colored error output during build, fix for Markdown-formatted item subtitles.

2016-01-09: Version 0.1, initial release.
