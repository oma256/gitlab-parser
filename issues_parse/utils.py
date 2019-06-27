from datetime import datetime


def convert_date_to_second(request):
    start_time = request.GET['start-time']
    year, month, day = start_time.split('-')
    date = datetime(int(year), int(month), int(day))
    start_time_second = int(date.timestamp())

    start_time = request.GET['end-time']
    year, month, day = start_time.split('-')
    date = datetime(int(year), int(month), int(day))
    end_time_second = int(date.timestamp())

    return start_time_second, end_time_second


intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),  # 60 * 60 * 24
    ('hours', 3600),  # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)


def convert_second_to_datetime(second, granularity=2):
    result = []

    for name, count in intervals:
        value = second // count
        if value:
            second -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])
