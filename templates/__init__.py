"""
Templates package — all HTML template generators.
Import from here: `from templates import get_login_page_html, ...`
"""

from templates.auth_templates import get_login_page_html, get_register_page_html
from templates.hiragana_templates import get_hiragana_table_html
from templates.katakana_templates import get_katakana_table_html
from templates.profile_templates import get_profile_page_html
from templates.achievements_templates import get_achievements_page_html

__all__ = [
    "get_login_page_html",
    "get_register_page_html",
    "get_hiragana_table_html",
    "get_katakana_table_html",
    "get_profile_page_html",
    "get_achievements_page_html",
]
