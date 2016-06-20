from datetime import datetime 

from django.test import TestCase

from . import util

class CommonUtilTestCase(TestCase):
    def setUp(self):
        pass

    def test_utcoffset_math(self):
        """Test utcoffset computation.

        See: http://www.worldtimebuddy.com/?pl=1&lid=100,8,658225,1850147&h=100
        """
        dt = datetime(2015, 11, 16,  1, 15, 24)
        self.assertEqual(util.utcoffset_where_hour_is(hour=17, relative_to_utc=dt), -8*3600)
        self.assertEqual(util.utcoffset_where_hour_is(hour=3, relative_to_utc=dt),  +2*3600)
        self.assertEqual(util.utcoffset_where_hour_is(hour=10, relative_to_utc=dt), +9*3600)

        dt = datetime(2015, 11, 16, 19, 15, 24)
        self.assertEqual(util.utcoffset_where_hour_is(hour=11, relative_to_utc=dt), -8*3600)
        self.assertEqual(util.utcoffset_where_hour_is(hour=21, relative_to_utc=dt), +2*3600)
        self.assertEqual(util.utcoffset_where_hour_is(hour=4, relative_to_utc=dt),  +9*3600)

        dt = datetime(2015, 11, 16, 23, 15, 24)
        self.assertEqual(util.utcoffset_where_hour_is(hour=15, relative_to_utc=dt), -8*3600)
        self.assertEqual(util.utcoffset_where_hour_is(hour=1, relative_to_utc=dt), +2*3600)
        self.assertEqual(util.utcoffset_where_hour_is(hour=8, relative_to_utc=dt),  +9*3600)
        self.assertEqual(util.utcoffset_where_hour_is(hour=0, relative_to_utc=dt),  +1*3600)
