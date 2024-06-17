import pandas as pd
import datetime as dt
import tcxreader


def tcx_parse(filepath):
    parser = tcxreader.TCXReader()

    file = parser.read(filepath)

    df = pd.DataFrame()

    date = []
    time_raw = []
    time_total_seconds = []
    heart_rate = []
    latitude = []
    longitude = []
    elevation = []
    distance_meters = []

    for iterr, trackpoint in enumerate(file.trackpoints):
        date.append(str(trackpoint.time.date()))
        time_raw.append(str(trackpoint.time.time()))
        time_total_seconds.append(iterr)
        heart_rate.append(trackpoint.hr_value)
        latitude.append(trackpoint.latitude)
        longitude.append(trackpoint.longitude)
        elevation.append(trackpoint.elevation)

        if trackpoint.distance > 0:
            last_distance = trackpoint.distance

        if trackpoint.distance == 0 and iterr > 0:
            try:
                distance_meters.append(last_distance)
            except UnboundLocalError:
                last_distance = 0
                distance_meters.append(last_distance)
        else:
            distance_meters.append(trackpoint.distance)

    df['Date'] = date
    df['Time (24 Hour Clock)'] = time_raw
    df['Time (Seconds)'] = time_total_seconds
    df['Heart Rate'] = heart_rate
    df['Latitude'] = latitude
    df['Longitude'] = longitude
    df['Elevation (Meters)'] = elevation
    df['Distance (Meters)'] = distance_meters

    return df


def calculate_change(df, orig_name, new_name):
    df[new_name] = pd.NA

    for index, value in enumerate(df[orig_name]):
        if index == 0:
            df.at[index, new_name] = 0
        else:
            prev = df.at[index - 1, orig_name]
            df.at[index, new_name] = value - prev

    return df


def convert(df):
    cols = ['Date', 'Time (24 Hour Clock)', 'Time (Seconds)',
            'Time (Hour-Minute-Second)', 'Latitude', 'Longitude',
            'Elevation (Meters)', 'Elevation Change (Meters)',
            'Elevation (Feet)', 'Elevation Change (Feet)', 'Distance (Meters)',
            'Distance (Kilometers)', 'Distance (Miles)',
            'Pace (Minutes / Mile)', 'Pace (Numeric)', 'Heart Rate']

    df['Time (Hour-Minute-Second)'] = pd.NA
    df['Elevation (Feet)'] = df['Elevation (Meters)'] * 3.280839895
    df['Elevation Change (Meters)'] = pd.NA
    df['Elevation Change (Feet)'] = pd.NA
    df['Distance (Kilometers)'] = df['Distance (Meters)'] / 1000
    df['Distance (Miles)'] = df['Distance (Meters)'] / 1609.344
    df['Pace (Minutes / Mile)'] = pd.NA
    df['Pace (Numeric)'] = pd.NA

    for index, value in enumerate(df['Time (Seconds)']):
        hours = value // 3600
        minutes = (value - (hours * 3600)) // 60
        seconds = value - (hours * 3600 + minutes * 60)

        df.at[index, 'Time (Hour-Minute-Second)'] = dt.time(hour=hours,
                                                            minute=minutes,
                                                            second=seconds)

    df = calculate_change(df,
                          'Elevation (Meters)',
                          'Elevation Change (Meters)')

    df = calculate_change(df,
                          'Elevation (Feet)',
                          'Elevation Change (Feet)')

    for index, value in enumerate(df['Distance (Miles)']):
        if index == 0:
            df.at[index, 'Pace (Minutes / Mile)'] = dt.time(hour=0,
                                                            minute=0,
                                                            second=0)
        else:
            prev = df.at[index - 1, 'Distance (Miles)']
            delta_dist = value - prev

            if delta_dist == 0:
                df \
                 .at[index,
                     'Pace (Minutes / Mile)'] = df \
                                                 .at[index - 1,
                                                     'Pace (Minutes / Mile)']
            else:
                val = (1 / delta_dist)
                hours = int(val // 3600)
                minutes = int((val - (hours * 3600)) // 60)
                seconds = int(val - (hours * 3600 + minutes * 60))
                df.at[index, 'Pace (Minutes / Mile)'] = dt.time(hour=hours,
                                                                minute=minutes,
                                                                second=seconds)

            print(f'Iterr: {index}, Value: {value}')
    
    df['Pace (Minutes / Mile)'] = pd.to_datetime(df['Pace (Minutes / Mile)'])
    df_hour = df['Pace (Minutes / Mile)'].dt.hour
    df_minutes = df['Pace (Minutes / Mile)'].dt.minute
    df_second = df['Pace (Minutes / Mile)'].dt.second
    
    df['Pace (Numeric)'] = df_hour + (df_minute / 60) + (df_second / 3600)

    df = df[cols]

    return df

