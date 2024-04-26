import pandas as pd
import os
import matplotlib.pyplot as plt
import warnings


def plot_event(data_directory, dates, coast, metadata, island='all'):
    """
    Plot up rainfall total for provided dates.
    :param files:
    :param dates:
    :param coast:
    :param meta:
    :param island: 'Hawaii', 'Kahoolawe', 'Kauai', 'Lanai', 'Maui', 'Molokai', 'Oahu'
    :return:
    """
    if island == 'all':
        warnings.filterwarnings("ignore", message="Columns (4) have mixed types.")
        files = [f'{data_directory}/{f}.csv' for f in metadata.FILENAME]
        df_list = list_clipped_stations(files, dates)
        rf_totals = [df.RF_mm.sum() for df in df_list if df is not None]
        coordinates = [(metadata.LON.iloc[cnt], metadata.LAT.iloc[cnt]) for cnt, df in enumerate(df_list) if df is not None]
        lons = [coord[0] for coord in coordinates]
        lats = [coord[1] for coord in coordinates]
    else:
        index = metadata.ISLAND == island
        index_coast = coast.isle == island
        coast = coast.loc[index_coast]
        metadata = metadata.loc[index]
        warnings.filterwarnings("ignore", message="Columns (4) have mixed types.")
        files = [f'{data_directory}/{f}.csv' for f in metadata.FILENAME]
        df_list = list_clipped_stations(files, dates)
        rf_totals = [df.RF_mm.sum() for df in df_list if df is not None]
        coordinates = [(metadata.LON.iloc[cnt], metadata.LAT.iloc[cnt]) for cnt, df in enumerate(df_list) if df is not None]
        lons = [coord[0] for coord in coordinates]
        lats = [coord[1] for coord in coordinates]

    fig, ax = plt.subplots()
    coast.plot(ax=ax, edgecolor='black', facecolor='none')
    plt.scatter(lons, lats, c=rf_totals)

    return ax,rf_totals,lats,lons


def list_clipped_stations(files, dates):
    """
    Returns a list of dataframes (one for each station) clipped by the date range.
    :param dates:
    :return:
    """
    list_df = [clip_station(f,dates) for f in files]
    return  list_df


def clip_station(station_file, dates):
    """

    :param station_file:
    :return:
    """
    if os.path.exists(station_file):
        df = pd.read_csv(station_file)
        df['DateTime'] = pd.to_datetime(df['DateTime'])

        min_d = min(dates)
        max_d = max(dates)

        index = (df['DateTime'] >= min_d) & (df['DateTime'] <= max_d)

        return df.loc[index]
    else:
        print(f"Cannot find file: {station_file}, skipping...")
        return 