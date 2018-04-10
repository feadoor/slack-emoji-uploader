# -*- encoding: utf-8 -*-

import pytest
from bs4 import BeautifulSoup as BSoup

from slack_emoji_uploader import beautiful_soup_helper


@pytest.mark.parametrize('html, name, expected', [
    # A single <input/> tag with a value
    ('<input name="alexander" value="armstrong" />', 'alexander', 'armstrong'),
    # A single <input/> tag with no value
    ('<input name="brutus" />', 'brutus', None),
    # No <input/> tags
    ('<body><p>Not an input</p></body>', 'caesar', None),
    # Multiple matching <input/> tags
    ('<input name="daedalus" value="diggle" /><input name=daedalus value=duck />', 'daedalus', 'diggle'),
    # A single non-matching <input/> tag
    ('<input name="ernie" value="els" />', 'eric', None),
    # Multiple <input/> tags of which the second matches
    ('<input name="fiona" value="finnegan" /><input name="fred" value="forsyth" />', 'fred', 'forsyth'),
    # Multiple <input/> tags of which none match
    ('<input name="godfrey" value="goodwood" /><input name="grayson" value="gray" />', 'george', None),
])
def test_get_input_value(html, name, expected):
    parsed_html = BSoup(html, 'html.parser')
    assert beautiful_soup_helper.get_input_value(parsed_html, name) == expected


@pytest.mark.parametrize('html, expected', [
    # A single page error
    ('<p class="alert_error"><i>Awful!</i></p>', 'Awful!'),
    # No errors
    ('<p class="alert_warn"><i>Bad!</i></p>', None),
    # Multiple errors
    ('<p class="alert_error">Contemptible!</p><p class="alert_error">Curses!</p>', 'Contemptible!'),
])
def test_get_page_error(html, expected):
    parsed_html = BSoup(html, 'html.parser')
    assert beautiful_soup_helper.get_page_error(parsed_html) == expected
