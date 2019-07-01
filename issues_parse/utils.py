from datetime import datetime


def convert_date_to_second(request):
    """
    converts to seconds coming with request object (start-time, end-time)
    :param request:
    :return:
    """
    start_time = request.GET['start-time']
    year, month, day = start_time.split('-')
    date = datetime(int(year), int(month), int(day))
    start_time_of_seconds = int(date.timestamp())

    start_time = request.GET['end-time']
    year, month, day = start_time.split('-')
    date = datetime(int(year), int(month), int(day))
    end_time_of_seconds = int(date.timestamp())

    return start_time_of_seconds, end_time_of_seconds


intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),  # 60 * 60 * 24
    ('hours', 3600),  # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)


def convert_second_to_datetime(seconds, granularity=2):
    """
    converts seconds to datetime
    :param seconds:
    :param granularity:
    :return:
    """
    result = []

    for measurement_name, seconds_count in intervals:
        value = seconds // seconds_count
        if value:
            seconds -= value * seconds_count
            if value == 1:
                measurement_name = measurement_name.rstrip('s')
            result.append("{} {}".format(value, measurement_name))
    return ', '.join(result[:granularity])


def sum_working_hours(work_logs, start_time, end_time):
    sum_seconds = 0

    for work_log in work_logs:
        if work_log.get_create_at in range(start_time, end_time):
            sum_seconds += work_log.get_time_spend

    total_time = convert_second_to_datetime(sum_seconds)

    return str(total_time)
