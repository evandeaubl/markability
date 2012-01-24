#!/usr/bin/env python2

from readability.readability import Document
from readability.htmls import build_doc
import urllib2
import html2text

def markdownify(url_list, **options):
    articles = []
    images = []
    paragraph_links = options['paragraph_links']
    wrap_text = options['wrap_text']
    preamble = options['preamble']
    for url in url_list:
        req = urllib2.Request(url,None,{'Referer': url_list[0]})
        html = urllib2.urlopen(req).read()
        document = Document(html, url=url)
        readable_title = document.short_title()
        summary = document.summary()
        summary_doc = build_doc(summary)
        images.extend([a.get('src') for a in summary_doc.findall('.//img')])
        articles.append(document.summary())

    markdown_articles = []
    if preamble:
        markdown_articles.append("Article title: %s\nOriginal URL: %s" % (readable_title, url_list[0]))
    for (article, url) in zip(articles, url_list):
        h = html2text.HTML2Text(baseurl=url)
        h.inline_links = False
        h.links_each_paragraph = (paragraph_links and 1) or 0
        h.body_width = (wrap_text and 78) or 0
        markdown_articles.append(h.handle(article))
    return u"\n\n----\n\n".join(markdown_articles).encode("utf-8")
