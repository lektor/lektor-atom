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
[My Blog]
source_path = /
url_path = /feed.xml
items = site.query('/').filter(F.type == 'post')
item_model = blog-post

[My Blog: Coffee Articles]
source_path = /
url_path = /category/python/feed.xml
items = site.query('/blog').filter(F.categories.contains('coffee'))
item_model = blog-post
```

### Options

|Option               | Default    | Description
|---------------------|------------|-------------------------------------------------------------------------
|source\_path         | /          | Where in the content directory to find items' parent source
|filename             | feed.xml   | Name of generated Atom feed file
|url\_path            |            | Feed's URL on your site: default is source's URL path plus the filename
|blog\_author\_field  | author     | Name of source's author field
|blog\_summary\_field | summary    | Name of source's summary field
|items                | None       | A query expression: default is the source's children
|limit                | 50         | How many recent items to include
|item\_title\_field   | title      | Name of items' title field
|item\_body\_field    | body       | Name of items' content body field
|item\_author\_field  | author     | Name of items' author field
|item\_date\_field    | pub\_date  | Name of items' publication date field
|item\_model          | None       | Name of items' model

### Customizing the plugin for your models

Use the "_field" options to tell lektor-atom how to read your items. For example, if your site's model is:

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
blog_author_field = writer
blog_summary_field = short_description
```

### Filtering items

By default, lektor-atom gets the source at `source_path` and includes all its children in the feed. If you set `item_model`, lektor-atom includes only the children with that data model.

Set `items` to any query expression to override the default. If `items_model` is *also* specified, lektor-atom applies it as a filter to `items`.
