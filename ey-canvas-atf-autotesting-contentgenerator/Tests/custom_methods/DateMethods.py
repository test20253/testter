import os
import datetime
from datetime import timedelta, datetime, date

class DateMethods:

    ZULU_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

    @staticmethod
    def is_this_previous_month(date):
        current_month = datetime.now().month
        month_of_input_date = datetime.datetime.strptime(date, "%m").month
        if (current_month != month_of_input_date):
            return False
        return True
    
    @staticmethod
    def get_current_datetime():
        current_datetime = datetime.now()
        return current_datetime
    
    @staticmethod
    def get_current_datetime_as_str(days=0, seconds=0, microseconds=0,
                milliseconds=0, minutes=0, hours=0, weeks=0, format='%Y-%m-%d %H:%M:%S'):

        """
         Get the current datetime as a formatted string.
        Args:
            seconds (int):
            microseconds(int):
            milliseconds(int):
            minutes(int):
            hours(int):
            weeks(int):
            format (str): Format string for the output datetime.
        Returns: 
            str: Formatted datetime string.
        """
        date_data = datetime.utcnow() + timedelta(days=days, seconds=seconds, microseconds=microseconds,
                milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)
        return date_data.strftime(format)

    @staticmethod
    def get_current_datetime_as_ISO8601(days=0, seconds=0, microseconds=0,
                                    milliseconds=0, minutes=0, hours=0, weeks=0, format=None):
        now = datetime.now()
        delta = timedelta(days=days, seconds=seconds, microseconds=microseconds,
                          milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)
        adjusted_datetime = now + delta
        if format is None:
            return adjusted_datetime.isoformat()
        return adjusted_datetime.strftime(format)