# coding:utf-8

import mistune

_markdown = mistune.Markdown(escape=True, hard_wrap=True)


def render(text):
    return _markdown(text)
