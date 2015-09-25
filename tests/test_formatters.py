# -*- coding: utf-8 -*-
import datetime
import json
import logging

from logging_json_formatter.formatters import AppendJSONFormatter


def test_limit_keys_to():
    formatter = AppendJSONFormatter(limit_keys_to=('foo', 'bar'))
    record = get_record(extra={'foo': 'yes', 'bar': 'yes', 'baz': 'no'})
    output = formatter.format(record)
    assert output.count('yes') == 2
    assert output.count('no') == 0

    data = json.loads(formatter.get_json(record))
    assert data['foo'] == 'yes'
    assert data['bar'] == 'yes'
    assert 'baz' not in data


def test_force_keys():
    formatter = AppendJSONFormatter(force_keys=('lineno', 'levelname'))
    record = get_record(extra={'foo': 'yes', 'bar': 'yes', 'baz': 'no'})
    output = formatter.format(record)
    assert 'levelname' in output
    assert 'lineno' in output


def test_empty_extra():
    formatter = AppendJSONFormatter(limit_keys_to=('foo',))
    record = get_record(extra={'bar': 'no'})
    output = formatter.format(record)
    # empty json should not lead to excess whitespace at the end of the line
    assert not output.endswith(' ')
    assert formatter.get_json(record) == ''


def test_repr_fail():
    class A:
        def __repr__(self):
            raise ValueError

    formatter = AppendJSONFormatter()
    record = get_record(extra={'a': A()})
    output = formatter.format(record)
    assert AppendJSONFormatter.REPR_FAIL_PLACEHOLDER in output


def test_json_dumps_fail():
    class FailFormatter(AppendJSONFormatter):
        BASE_TYPES = (datetime.datetime,)

    formatter = FailFormatter()
    record = get_record(extra={'d': datetime.datetime(2015, 1, 1, 0, 0, 1)})
    output = formatter.format(record)
    assert 'formatter_error' in output


def get_record(name='foo', level=logging.INFO, pathname='/foo/bar', lineno=42,
               msg='Foo! Bar!', args=None, exc_info=None, extra=None):
    record = logging.LogRecord(name, level, pathname, lineno, msg, args, exc_info)
    if extra:
        for key, val in extra.items():
            setattr(record, key, val)
    return record
