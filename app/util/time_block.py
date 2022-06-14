def validate_one_end_of_time_block(value: str):
    seperated_block = value.replace(' ', '').split(':')
    if len(seperated_block) != 2:
        raise ValueError
    hour, minute = seperated_block
    if not hour.isnumeric() or not minute.isnumeric():
        raise ValueError
    hour, minute = int(hour), int(minute)
    if hour > 23 or hour < 0 or minute < 0 or minute > 59:
        raise ValueError
    return hour, minute


def validate_time_block(value: str):
    """ Validator for single time block

        Parameters
        ----------
        value: str
            The string of time block. For example: '1:00 - 13:00'

        Raises
        ---------
        ValueError
            If the value is not qualified a time block

        Returns
        ---------
        set
            A set of two elements (begin, end) represents minutes of begin and end
    """
    seperated_block = value.replace(' ', '').split('-')
    if len(seperated_block) != 2:
        raise ValueError
    begin, end = seperated_block
    begin_hour, begin_minute = validate_one_end_of_time_block(begin)
    end_hour, end_minute = validate_one_end_of_time_block(end)
    begin_timestamp = begin_hour * 60 + begin_minute
    end_timestamp = end_hour * 60 + end_minute
    if begin_timestamp > end_timestamp:
        raise ValueError
    return begin_timestamp, end_timestamp
