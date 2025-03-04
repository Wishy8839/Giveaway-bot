import datetime
import re





def current_time_in_unix():
    return int(datetime.datetime.timestamp(datetime.datetime.now()))



def seconds_to_time(secs: float):
    days = datetime.timedelta(seconds=secs).days
    hours = datetime.timedelta(seconds=secs).seconds
    return days, hours

def unix_to_time(unix: float):
    return datetime.datetime.fromtimestamp(unix)

def seconds_to_time(seconds: float):
    date_time = datetime.datetime.fromtimestamp(seconds)
    return date_time.strftime("%m/%d/%Y %H:%M:%S")

def seconds_to_discord_timestamp(seconds: float):
    current = current_time_in_unix() 
    seconds = string_to_seconds(seconds)
    total = current + seconds
    return f"<t:{total}:f>"




# not all made by me (im too lazy)
def string_to_seconds(time_str):
    time_str = str(time_str)
    time_str = time_str.lower()
    total_seconds = 0
    
    time_units = {
        "month": 2628288,
        "day": 86400,
        "hour": 3600,
        "minute": 60,
        "second": 1
    }


    if time_str.isdigit():
        return int(time_str)


    # Check if it's in MM/DD/YYYY format
    date_match = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", time_str)
    if date_match:
        month, day, year = map(int, date_match.groups())
        try:
            target_date = datetime.datetime(year, month, day)
            current_date = datetime.datetime.now()
            delta_seconds = (target_date - current_date).total_seconds()
            if delta_seconds > 8035200 or delta_seconds < 0:
                return False
            return int(delta_seconds)
        except ValueError:
            return False
    
    
    matches = re.findall(r"(\d+)\s*(months?|days?|hours?|minutes?|seconds?)", time_str)
    if not matches:
        return False
    
    for value, unit in matches:
        unit = unit.rstrip("s") 
        if unit not in time_units:
            return False
        total_seconds += int(value) * time_units[unit]
    
    if total_seconds > 8035200: # 8035200 is 3 months btw
        return False
    
    return float(total_seconds)
