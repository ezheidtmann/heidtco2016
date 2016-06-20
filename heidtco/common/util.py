from datetime import datetime, timedelta, tzinfo

def textify(d):
    return ' '.join(['{}={}'.format(k, v) for k, v in d.iteritems()])

def get_week_start_day(dt, firstday='monday'):
    if firstday == 'monday':
        return dt.date() - timedelta(days=(dt.weekday() + 0)%7)
    elif firstday == 'sunday':
        return dt.date() - timedelta(days=(dt.weekday() + 1)%7)

class OffsetTZ(tzinfo):
    def __init__(self, offset_seconds):
        self._offset_seconds = int(offset_seconds)
    def utcoffset(self, dt):
        return timedelta(seconds=self._offset_seconds)
    def dst(self, dt):
        return timedelta(0)
    def tzname(self, dt):
        return ''

def conditions_sql(conditions):
    """Get SQL text ready for a WHERE clause.

    Examples:
      "(something_about_time)"
      "(something_about_time) AND (something_about_start_point)"
      "(something_about_time) AND (something_about_start_point) AND (something_about_via)"
    """
    sql = ") AND (".join(conditions)
    if len(sql) > 0:
        return '(' + sql + ')'
    return '(1 = 1)'

def sha256_sorted_json(thing):
    import hashlib
    import json
    return hashlib.sha256(json.dumps(thing, sort_keys=True)).hexdigest()

def get_all_subclasses(cls):
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses

def utcoffset_where_hour_is(hour=2, relative_to_utc=None):
    if relative_to_utc is None:
        relative_to_utc = datetime.utcnow()
    if hour > relative_to_utc.hour:
        td = timedelta(hours=hour - relative_to_utc.hour)
    else:
        td = timedelta(hours=24 + hour - relative_to_utc.hour)

    utcoffset = abs(int(td.total_seconds()))
    if utcoffset > 43200:
        return utcoffset - 86400
    return utcoffset
