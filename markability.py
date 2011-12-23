#!/usr/bin/env python2

from readability.readability import Document
from readability.htmls import build_doc
import urllib2
import html2text

def markdownify(url_list):
    articles = []
    images = []
    for url in url_list:
        req = urllib2.Request(url,None,{'Referer': url_list[0]})
        html = urllib2.urlopen(req).read()
        document = Document(html, url=url)
#        readable_title = document.short_title()
        summary = document.summary()
        summary_doc = build_doc(summary)
        images.extend([a.get('src') for a in summary_doc.findall('.//img')])
        articles.append(document.summary())

    markdown_articles = []
    for article in articles:
        h = html2text.HTML2Text()
        h.inline_links = False
        markdown_articles.append(h.handle(article))
    return u"\n\n----\n\n".join(markdown_articles).encode("utf-8")
