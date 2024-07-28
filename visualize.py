import pandas as pd
import numpy as np
import math
import folium
import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime, timedelta


def customizable_lineplot(x, y,
                          title='Line Plot', xlabel='X-axis', ylabel='Y-axis',
                          line_style='-', line_color='b', line_width=2,
                          marker='', marker_size=5, marker_color='b',
                          grid=True, grid_style='--', grid_color='gray',
                          grid_alpha=0.7,
                          xlim=None, ylim=None, legend_label=None,
                          legend_loc='best',
                          figsize=(10, 6), save_path=None):
    # plt.figure(figsize=figsize)

    plt.plot(x, y, linestyle=line_style, color=line_color,
             linewidth=line_width,
             marker=marker, markersize=marker_size,
             markerfacecolor=marker_color)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if grid:
        plt.grid(True, linestyle=grid_style, color=grid_color,
                 alpha=grid_alpha)

    if xlim:
        plt.xlim(xlim)

    if ylim:
        plt.ylim(ylim)

    if legend_label:
        plt.legend([legend_label], loc=legend_loc)

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    else:
        plt.show()


def plot_route(filename=[], dates=None, start_zoom=15):
    months = {'01': 'January', '02': 'February', '03': 'March', '04': 'April',
              '05': 'May', '06': 'June', '07': 'July', '08': 'August',
              '09': 'September', '10': 'October', '11': 'November',
              '12': 'December'}

    for file in filename:
        os.chdir('..')
        os.chdir(os.getcwd() + '\\csv')

        df = pd.read_csv(file)

        if dates is None:
            dates = df['Date'].unique().tolist()

        dates = [x for x in dates if
                 df[df['Date'] == x].iloc[0, 15] == 'TCX']

        for date in dates:
            print(f'Processing {file} {date}...')

            df_date = df.copy()
            df_date = df_date[df_date['Date'] == date].reset_index()

            df_date['Pace (Numeric)'] = pd.NA

            for index, val in enumerate(df_date['Pace (Numeric)']):
                hour = int(df_date['Pace (Minutes / Mile)']
                           [index][0:2])
                minute = int(df_date['Pace (Minutes / Mile)']
                             [index][3:5])
                second = int(df_date['Pace (Minutes / Mile)']
                             [index][6:8])

                pace_numeric = (hour * 3600) + (minute * 60) + second

                df_date.at[index, 'Pace (Numeric)'] = pace_numeric

            m = folium.Map(
                location=[df_date['Latitude'].iloc[0],
                          df_date['Longitude'].iloc[0]],
                zoom_start=start_zoom)

            fg_hr = folium.FeatureGroup(name='Heart Rate')
            fg_pace = folium.FeatureGroup(name='Pace')
            fg_el = folium.FeatureGroup(name='Elevation')

            distance = df_date['Distance (Miles)']
            heart_rates = df_date['Heart Rate']
            pace = df_date['Pace (Numeric)']
            pace_org = pace.copy()
            pace_dt = df_date['Pace (Minutes / Mile)']
            el = df_date['Elevation (Feet)']

            pace_mean = pace.mean()
            pace_q1 = np.percentile(pace, 0.1)
            pace_q3 = np.percentile(pace, 98.7)

            for index, val in enumerate(pace):
                if not (pace_q1 < val < pace_q3):
                    pace.at[index] = pace_mean
                pace.at[index] = pace.at[index] * -1

            norm_hr = plt.Normalize(vmin=heart_rates.min(),
                                    vmax=heart_rates.max())
            norm_p = plt.Normalize(vmin=pace.min(), vmax=pace.max())
            norm_el = plt.Normalize(vmin=el.min(), vmax=el.max())

            cmap = plt.get_cmap('coolwarm')

            for i in range(len(df_date) - 1):
                # Add PolyLines for each plot type
                color = cmap(norm_hr(heart_rates.iloc[i]))
                color = mcolors.to_hex(color)
                poly_hr = folium.PolyLine(
                    locations=[(df_date.iloc[i]['Latitude'],
                                df_date.iloc[i]['Longitude']),
                               (df_date.iloc[i]['Latitude'],
                                df_date.iloc[i]['Longitude'])],
                    color=color,
                    weight=5,
                    tooltip=folium.Tooltip(f"Heart Rate: "
                                           f"{heart_rates.iloc[i]}")
                )
                poly_hr.add_to(fg_hr)

                color = cmap(norm_p(pace.iloc[i]))
                color = mcolors.to_hex(color)
                poly_pace = folium.PolyLine(
                    locations=[(df_date.iloc[i]['Latitude'],
                                df_date.iloc[i]['Longitude']),
                               (df_date.iloc[i]['Latitude'],
                                df_date.iloc[i]['Longitude'])],
                    color=color,
                    weight=5,
                    tooltip=folium.Tooltip(f"Pace: {pace_dt.iloc[i]}")
                )
                poly_pace.add_to(fg_pace)

                color = cmap(norm_el(el.iloc[i]))
                color = mcolors.to_hex(color)
                poly_el = folium.PolyLine(
                    locations=[(df_date.iloc[i]['Latitude'],
                                df_date.iloc[i]['Longitude']),
                               (df_date.iloc[i]['Latitude'],
                                df_date.iloc[i]['Longitude'])],
                    color=color,
                    weight=5,
                    tooltip=folium.Tooltip(f"Elevation: {el.iloc[i]}")
                )
                poly_el.add_to(fg_el)

                if (distance[i] > 0 and
                    (math.floor(distance[i]) -
                     math.floor(distance[i - 1]) == 1)):
                    avg_hr = heart_rates.iloc[:i].mean()
                    avg_pace = pace_org.iloc[:i].mean()
                    avg_el = el.iloc[:i].mean()

                    avg_hours = avg_pace // 3600
                    avg_minutes = avg_pace // 60
                    avg_seconds = math \
                        .floor(avg_pace - avg_minutes * 60)

                    avg_pace_str = timedelta(hours=avg_hours,
                                             minutes=avg_minutes,
                                             seconds=avg_seconds)
                    avg_pace_str = str(avg_pace_str)

                    marker_hr = folium.Marker(
                        location=[df_date.iloc[i]['Latitude'],
                                  df_date.iloc[i]['Longitude']],
                        popup=folium.Popup(
                            f"Distance: {math.floor(distance[i])} mi, "
                            f"Avg Heart Rate: {avg_hr:.2f} bpm, "
                            f"Avg Pace: {avg_pace_str} min/mile, "
                            f"Avg Elevation: {avg_el:.2f} ft",
                            max_width=500
                        )
                    )
                    marker_hr.add_to(fg_hr)

                    marker_pace = folium.Marker(
                        location=[df_date.iloc[i]['Latitude'],
                                  df_date.iloc[i]['Longitude']],
                        popup=folium.Popup(
                            f"Distance: {math.floor(distance[i])} mi, "
                            f"Avg Heart Rate: {avg_hr:.2f} bpm, "
                            f"Avg Pace: {avg_pace_str} min/mile, "
                            f"Avg Elevation: {avg_el:.2f} ft",
                            max_width=500
                        )
                    )
                    marker_pace.add_to(fg_pace)

                    marker_el = folium.Marker(
                        location=[df_date.iloc[i]['Latitude'],
                                  df_date.iloc[i]['Longitude']],
                        popup=folium.Popup(
                            f"Distance: {math.floor(distance[i])} mi, "
                            f"Avg Heart Rate: {avg_hr:.2f} bpm, "
                            f"Avg Pace: {avg_pace_str} min/mile, "
                            f"Avg Elevation: {avg_el:.2f} ft",
                            max_width=500
                        )
                    )
                    marker_el.add_to(fg_el)

            fg_hr.add_to(m)
            fg_pace.add_to(m)
            fg_el.add_to(m)

            folium.LayerControl().add_to(m)

            os.chdir('..')
            os.chdir(os.getcwd() + '\\visualize\\routes')
            os.makedirs(file[0:-4], exist_ok=True)
            os.chdir(os.getcwd() + f'\\{file[0:-4]}')
            m.save(os.path.join(os.getcwd(),
                                f'{months[date[5:7]]}_{date[8:10]}.html'))
            os.chdir(os.path.dirname(os.path.abspath(__file__)))