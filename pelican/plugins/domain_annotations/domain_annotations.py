"""This plug-in adds domain annotations to hyperlinks."""

import logging
import re

from typing import Union

from pelican import ArticlesGenerator, PagesGenerator, signals  # type: ignore
from pelican.contents import Article, Page  # type: ignore

logger = logging.getLogger(__name__)

RE_LINK = re.compile(
    r"""
        (
            <a
            \s
            [^>]*?
            href="
                [a-z0-9]+
                :///?
                [a-z0-9-_.@]+
                .*?
            "
            [^>]*?
            >
            [^<]*?
            </a>
        )
    """,
    re.IGNORECASE | re.VERBOSE,
)

RE_LINK_EXTRACT_PARTS = re.compile(
    r"""
        <a
        \s
        [^>]*?
        href="
            [a-z0-9]+
            :///?
            ([a-z0-9-_.@]+)
            .*?
        "
        [^>]*?
        >
        ([^<]*?)
        </a>
    """,
    re.IGNORECASE | re.VERBOSE,
)


def generate_domain_annotations(item: Union[Article, Page]) -> None:
    """Process the hyperlinks on an article or page."""
    # pylint: disable=protected-access
    new_content = ""

    for part in RE_LINK.split(item._content):
        match = RE_LINK_EXTRACT_PARTS.search(part)

        if match:
            # Only annotate the domain if it's not already contained in the link text
            anchor_tag = match.group(0)
            domain = match.group(1)
            link_text = match.group(2)

            # Don't mind www.
            clean_domain = domain[4:] if domain.startswith("www.") else domain

            if not clean_domain in link_text:
                logger.debug("Annotating domain: %s", domain)
                part = f'{anchor_tag} <span class="domain">({domain})</span>'

        new_content += part

    item._content = new_content


def process_articles(generator: ArticlesGenerator) -> None:
    """Process all articles."""
    list_names = [
        "articles",
        "translations",
        "hidden_articles",
        "hidden_translations",
        "drafts",
        "drafts_translations",
    ]

    for list_name in list_names:
        item_list = getattr(generator, list_name)

        for item in item_list:
            generate_domain_annotations(item)


def process_pages(generator: PagesGenerator) -> None:
    """Process all pages."""
    list_names = [
        "pages",
        "translations",
        "hidden_pages",
        "hidden_translations",
        "draft_pages",
        "draft_translations",
    ]

    for list_name in list_names:
        item_list = getattr(generator, list_name)

        for item in item_list:
            generate_domain_annotations(item)


def register() -> None:
    """Register the plug-in with Pelican."""
    signals.article_generator_finalized.connect(process_articles)
    signals.page_generator_finalized.connect(process_pages)
