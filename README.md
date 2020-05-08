# Lektor Atom Plugin

![Linux tests](https://github.com/lektor/lektor-atom/workflows/Linux%20tests/badge.svg)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Join the chat at https://gitter.im/lektor/lektor](https://badges.gitter.im/lektor/lektor.svg)](https://gitter.im/lektor/lektor?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Builds one or more Atom XML feeds for your [Lektor](https://www.getlektor.com/)-based site.

Inspired by the [atom-feed-support](https://github.com/lektor/lektor-website/tree/master/packages/atom-feed-support) plugin Armin Ronacher wrote for the Lektor official blog.

## Installation

Add lektor-atom to your project from command line:

```sh
lektor plugins add lektor-atom
```

See [the Lektor documentation for more instructions on installing plugins](https://www.getlektor.com/docs/plugins/).

## Configuration

Here is a basic configuration:

```ini
[feed]
name = My Site's Blog
source_path = /blog
url_path = /feed.xml
```

For each feed you want to publish, add a section to `configs/atom.ini`. For example, a blog with a feed of all recent posts, and a feed of recent posts about coffee:

```ini
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

|Option               | Default    | Description
|---------------------|------------|-------------------------------------------------------------------------
|source\_path         | /                      | Where in the content directory to find items' parent source
|name                 | config section name    | Feed name
|filename             | feed.xml               | Name of generated Atom feed file
|url\_path            | source_path + filename | Feed's URL on your site
|blog\_author\_field  | author                 | Name of source's author field
|blog\_summary\_field | summary                | Name of source's summary field
|items                | source_path's children | A query expression: e.g. `site.query('/').filter(F.type == 'post')`
|limit                | 50                     | How many recent items to include
|item\_title\_field   | title                  | Name of items' title field
|item\_body\_field    | body                   | Name of items' content body field
|item\_author\_field  | author                 | Name of items' author field
|item\_date\_field    | pub\_date              | Name of items' publication date field
|item\_model          | None                   | Filters `items` on name of items' model

### Customizing the plugin for your models

Use the field options to tell lektor-atom how to read your items. For example, if your site's model is:

```ini
[model]
name = Blog

[fields.writer]
type = string

[fields.short_description]
type = string
```

Then add to atom.ini:

```ini
[main]
blog_author_field = writer
blog_summary_field = short_description
```

See [tests/demo-project/configs/atom.ini](https://github.com/ajdavis/lektor-atom/blob/master/tests/demo-project/configs/atom.ini) for a complete example.

### Filtering items

By default, lektor-atom gets the source at `source_path` and includes all its children in the feed. If you set `item_model`, lektor-atom includes only the children with that data model.

Set `items` to any query expression to override the default. If `items_model` is *also* specified, lektor-atom applies it as a filter to `items`.

## Use In Templates

You can link to a specific feed in your template. If your `atom.ini` contains a feed like this:

```ini
[main]
source_path = /blog
```

Link to the feed in a template like this:

```
{{ '/blog@atom/main'|url }}
```
