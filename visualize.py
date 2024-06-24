import pandas as pd
import folium
import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('..')
os.chdir(os.getcwd() + '\\csv')


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


def plot_route(df, date=None, start_zoom=15, filename=None, variance_factor=5):
    if date is not None:
        df = df[df['Date'] == date]

    m_hr = folium.Map(location=[df['Latitude'].iloc[0],
                                df['Longitude'].iloc[0]],
                      zoom_start=start_zoom)
    m_p = folium.Map(location=[df['Latitude'].iloc[0],
                               df['Longitude'].iloc[0]],
                     zoom_start=start_zoom)
    m_el = folium.Map(location=[df['Latitude'].iloc[0],
                                df['Longitude'].iloc[0]],
                      zoom_start=start_zoom)

    heart_rates = df['Heart Rate']
    pace = df['Pace (Numeric)']
    el = df['Elevation Change (Meters)']

    print(f"Heart Rate Range: {heart_rates.min()} - {heart_rates.max()}")
    print(f"Pace Range: {pace.min()} - {pace.max()}")
    print(f"Elevation Change Range: {el.min()} - {el.max()}")

    norm_hr = plt.Normalize(vmin=heart_rates.min(), vmax=heart_rates.max())
    pace_mean = pace.mean()
    el_mean = el.mean()

    norm_pace = plt.Normalize(
        vmin=pace_mean - variance_factor * (pace_mean - pace.min()),
        vmax=pace_mean + variance_factor * (pace.max() - pace_mean))
    norm_el = plt.Normalize(
        vmin=el_mean - variance_factor * (el_mean - el.min()),
        vmax=el_mean + variance_factor * (el.max() - el_mean))

    cmap = plt.get_cmap('coolwarm')

    for i in range(len(df) - 1):
        color = cmap(norm_hr(heart_rates.iloc[i]))
        color = mcolors.to_hex(color)
        folium.PolyLine(
            locations=[(df.iloc[i]['Latitude'], df.iloc[i]['Longitude']),
                       (df.iloc[i + 1]['Latitude'],
                        df.iloc[i + 1]['Longitude'])],
            color=color,
            weight=5
        ).add_to(m_hr)

        color = cmap(norm_pace(pace.iloc[i]))
        color = mcolors.to_hex(color)
        folium.PolyLine(
            locations=[(df.iloc[i]['Latitude'], df.iloc[i]['Longitude']),
                       (df.iloc[i + 1]['Latitude'],
                        df.iloc[i + 1]['Longitude'])],
            color=color,
            weight=5
        ).add_to(m_p)

        color = cmap(norm_el(el.iloc[i]))
        color = mcolors.to_hex(color)
        folium.PolyLine(
            locations=[(df.iloc[i]['Latitude'], df.iloc[i]['Longitude']),
                       (df.iloc[i + 1]['Latitude'],
                        df.iloc[i + 1]['Longitude'])],
            color=color,
            weight=5
        ).add_to(m_el)

    m_hr.save(os.getcwd() + '\\' + 'hr.html')
    m_p.save(os.getcwd() + '\\' + 'p.html')
    m_el.save(os.getcwd() + '\\' + 'el.html')


df = pd.read_csv('June 1.csv')
plot_route(df=df, filename='June 1.html')
