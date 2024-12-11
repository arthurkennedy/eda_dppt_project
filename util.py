# zillow_analysis.py

import pandas as pd
import matplotlib.pyplot as plt

US_COUNTRY_REGION_ID=102001

def melt_zillow_dataset(df, id_fields, fields_to_drop=[], regions_to_drop=[US_COUNTRY_REGION_ID], date_col='Date', value_col='Value', index_field=None, drop_na=True):
    """
    melt
    """
    if len(fields_to_drop) > 0:
        df = df.drop(columns=fields_to_drop)

    if len(regions_to_drop) > 0:
        df.drop(df[df['RegionID'].isin(regions_to_drop)].index, inplace=True)
    
    # Reshape the data. Convert columns to rows using melt()
    df = df.melt(id_vars=id_fields, var_name=date_col, value_name=value_col)
    
    # Convert 'EestimationDate' to datetime type
    df[date_col] = pd.to_datetime(df[date_col])
    
    # Drop rows where 'Value' is null or zero
    if drop_na:
        df = df.dropna(subset=[value_col])

    if index_field:
        df.set_index(index_field, inplace=True)
    
    return df

def get_top_regions_by_mom_change(df, months=12, top_n=25, 
                                  date_col='EestimationDate', region_id_col='RegionID', region_name_col='RegionName', 
                                  mom_change_col='MoM_Change'):
    """
    Calculate the top regions with the highest average Month-over-Month (MoM) change over the last 'n' months.

    Parameters:
    - df: DataFrame containing the data.
    - months: Number of months to consider for the analysis (default is 12).
    - top_n: Number of top regions to return (default is 25).
    - date_col: Name of the column containing the date values (default is 'EestimationDate').
    - region_id_col: Name of the column containing the region ID (default is 'RegionID').
    - region_name_col: Name of the column containing the region name (default is 'RegionName').
    - mom_change_col: Name of the column containing the MoM change values (default is 'MoM_Change').

    Returns:
    - DataFrame with the top regions based on average MoM change.
    """
    # Get the current date (or the most recent date in the dataset)
    current_date = df[date_col].max()

    # Calculate the date 'n' months before the current date
    last_n_months = current_date - pd.DateOffset(months=months)

    # Filter the data for the last 'n' months
    df_last_n_months = df[df[date_col] >= last_n_months]

    # Calculate the average MoM change for each region within the last 'n' months
    avg_mom_last_n_months = df_last_n_months.groupby([region_id_col, region_name_col])[mom_change_col].mean().reset_index()

    # Sort the regions by average MoM change (highest to lowest)
    top_regions = avg_mom_last_n_months.sort_values(by=mom_change_col, ascending=False).head(top_n)

    return top_regions


def plot_top_regions_mom_change(top_regions, region_name_col='RegionName', mom_change_col='MoM_Change'):
    """
    Plot the top regions based on their average Month-over-Month (MoM) change.

    Parameters:
    - top_regions: DataFrame containing the top regions with MoM change.
    - region_name_col: Name of the column containing the region names (default is 'RegionName').
    - mom_change_col: Name of the column containing the MoM change values (default is 'MoM_Change').
    """
    plt.figure(figsize=(12, 8))
    plt.barh(top_regions[region_name_col], top_regions[mom_change_col], color='green')
    plt.xlabel('Average Month-over-Month Change (%)')
    plt.ylabel('Region')
    plt.title('Top Regions with the Highest Average MoM Growth')
    plt.gca().invert_yaxis()  # Invert y-axis to show highest values at the top
    plt.tight_layout()

    # Show the plot
    plt.show()

def plot_region_mom_change(region, region_name, region_date_col='EestimationDate', mom_change_col='MoM_Change'):
    # Plot the MoM Change for this region
    plt.figure(figsize=(10, 6))
    plt.plot(region[region_date_col], region[mom_change_col], marker='o', linestyle='-', color='b')
    plt.title(f'Month-over-Month Home Value Change for {region_name}')
    plt.xlabel('Date')
    plt.ylabel('Month-over-Month Change (%)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    
    # Show the plot
    plt.show()
