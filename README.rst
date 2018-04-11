The Slack Emoji Uploader
========================

This is a command-line tool for uploading custom emoji to Slack.

This functionality is not available through the Slack API, so instead,
this tool manually builds the HTTP requests that would be made if you
were to upload the emoji by hand through the Slack web UI.

Installation
------------

To install this script, first checkout the latest sources:

.. code-block:: console

    $ git clone https://github.com/feadoor/slack-emoji-uploader.git

Then install the script using `pip`:

.. code-block:: console

    $ pip install -e .

Or `pipsi`:

.. code-block:: console

    $ pipsi install -e .

Python 2.7 and Python 3.4+ are supported, and you may even find it works
on other versions too!

Usage
-----

You run the tool on the command line, passing the filenames of the emoji
that you want to upload:

.. code-block:: console

    $ slackmoji images/emoji1.png images/emoji2.png
    $ slackmoji images/*.png

The tool will then prompt you for your Slack subdomain, your email address
and your password before uploading each of your emoji. You can also pass some
or all of this information using the following syntaxes:

.. code-block:: console

    $ slackmoji images/emoji.png --subdomain sub --email e@mail.com --password abcdef
    $ slackmoji images/emoji.png -s sub -e e@mail.com -p abcdef

For usage information, see also:

.. code-block:: console

    $ slackmoji --help

Caveats
-------

* This tool does not use any of Slack's documented APIs, and as such, it is
  entirely possible that an update to Slack could cause this tool to simply
  stop working.

* Be aware that the emoji you upload must conform to Slack's rules for custom emoji:

  - No more than 128px in width or heigh
  - No more than 64K in size

License
-------

This project is licensed under the MIT license.
