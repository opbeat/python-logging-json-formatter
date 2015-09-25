import json
import logging

try:
  basestring
except NameError:  # pragma: no cover
  basestring = str


class BaseJSONFormatter(logging.Formatter):
    REPR_FAIL_PLACEHOLDER = 'REPR_FAILED'
    BASE_TYPES = (int, float, bool, basestring)
    default_exclude_attrs = {
        # python 2/3
        'args', 'name', 'msg', 'levelname', 'levelno', 'pathname', 'filename',
        'module', 'exc_info', 'exc_text', 'lineno', 'funcName', 'created',
        'msecs', 'relativeCreated', 'thread', 'threadName', 'processName',
        'process', 'getMessage', 'message',

        # python 3
        'stack_info',
    }

    def __init__(self, limit_keys_to=None, force_keys=None, **kwargs):
        super(BaseJSONFormatter, self).__init__(**kwargs)
        self.limit_keys_to = limit_keys_to
        if force_keys:
            self.exclude_attrs = self.default_exclude_attrs - set(force_keys)
        else:
            self.exclude_attrs = self.default_exclude_attrs

    def get_json(self, record):
        extra = {}
        for attr, value in record.__dict__.items():
            if ((self.limit_keys_to and attr in self.limit_keys_to) or
                    (not self.limit_keys_to and attr not in self.exclude_attrs)):
                if isinstance(value, self.BASE_TYPES):
                    extra[attr] = value
                else:
                    try:
                        extra[attr] = repr(value)
                    except Exception:
                        extra[attr] = self.REPR_FAIL_PLACEHOLDER
        if extra:
            try:
                return json.dumps(extra)
            except Exception as e:
                return json.dumps({
                    'formatter_error': repr(e),
                })
        return ''


class AppendJSONFormatter(BaseJSONFormatter):
    def format(self, record):
        formatted = super(BaseJSONFormatter, self).format(record)
        json_string = self.get_json(record)
        if json_string:
            return ' '.join([formatted, json_string])
        return formatted
