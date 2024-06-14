import pandas as pd
import folium
import os
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def customizable_lineplot(x, y,
                          title='Line Plot', xlabel='X-axis', ylabel='Y-axis',
                          line_style='-', line_color='b', line_width=2,
                          marker='', marker_size=5, marker_color='b',
                          grid=True, grid_style='--', grid_color='gray',
                          grid_alpha=0.7,
                          xlim=None, ylim=None, legend_label=None,
                          legend_loc='best',
                          figsize=(10, 6), save_path=None):
    plt.figure(figsize=figsize)

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


def plot_route(df, date=None, start_zoom=15, filename=None):
    if date is not None:
        df = df[df['Date'] == date]

    m = folium.Map(location=[df['Latitude'].iloc[0], df['Longitude'].iloc[0]],
                   zoom_start=start_zoom)

    folium.PolyLine(df[['Latitude', 'Longitude']].values, color='blue',
                    weight=5).add_to(m)

    folium.PolyLine(df[['Latitude', 'Longitude']].values, color='blue',
                    weight=5).add_to(m)

    m.save(os.getcwd() + '\\' + filename)
