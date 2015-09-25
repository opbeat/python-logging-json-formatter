=============================
python-logging-json-formatter
=============================

.. image:: https://img.shields.io/travis/opbeat/python-logging-json-formatter.svg
        :target: https://travis-ci.org/opbeat/python-logging-json-formatter

.. image:: https://img.shields.io/pypi/v/python-logging-json-formatter.svg
        :target: https://pypi.python.org/pypi/python-logging-json-formatter


A logging Formatter that appends extra data as JSON, e.g. for loggly

USAGE
--------

Using `dictConfig`
==================

.. code::

    import logging.config

    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'append_json': {
                '()': 'logging_json_formatter.AppendJSONFormatter',
                'format': '%(asctime)s %(name)s %(levelname)s %(funcName)s  %(filename)s:%(lineno)s %(message)s',

                # only use a specific set of keys
                'limit_keys_to': ['org_uuid', 'app_uuid'],

                # force keys that are ignored by default
                'force_keys': ('levelname', 'lineno'),
            }
        },
        'handlers': {
            'syslog': {
                'level': 'ERROR',
                'class': 'logging.handlers.SysLogHandler'
                'address': '/dev/log',
                'formatter': 'append_json'
            },
        },
    }
