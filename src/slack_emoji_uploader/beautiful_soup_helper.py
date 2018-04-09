# -*- encoding: utf-8 -*-
"""
Helper functions for extracting useful data from the parsed HTML responses
to the requests that we make to Slack.
"""


def get_input_value(soup, input_name):
        """
        Gets the `value` attribute of the first `input` element whose `name`
        attribute is equal to the given value.
        """
        input_element = soup.find('input', attrs={'name': input_name})
        if input_element is None or not input_element.has_attr('value'):
            return None
        return input_element['value']
