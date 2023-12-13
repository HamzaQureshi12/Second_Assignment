# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Define functions for reading and transposing data
def read_data_excel(excel_url, sheet_name, new_cols, countries):
    """
    Reads data from an Excel file and performs necessary preprocessing.

    Parameters:
    - excel_url (str): URL of the Excel file.
    - sheet_name (str): Name of the sheet containing data.
    - new_cols (list): List of columns to select from the data.
    - countries (list): List of countries to include in the analysis.

    Returns:
    - data_read (DataFrame): Preprocessed data.
    - data_transpose (DataFrame): Transposed data.
    """
    data_read = pd.read_excel(excel_url, sheet_name=sheet_name, skiprows=3)
    data_read = data_read[new_cols]
    data_read.set_index('Country Name', inplace=True)
    data_read = data_read.loc[countries]

    return data_read, data_read.T



# The Excel URL below indicates GDP growth (annual %)
excel_url_GDP = 'https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.KD.ZG?downloadformat=excel'

# The Excel URL below indicates arable land (% of land area)
excel_url_arable_land = 'https://api.worldbank.org/v2/en/indicator/AG.LND.ARBL.ZS?downloadformat=excel'

# The Excel URL below indicates forest area (% of land area)
excel_url_forest_area = 'https://api.worldbank.org/v2/en/indicator/AG.LND.FRST.ZS?downloadformat=excel'

# The Excel URL below indicates Urban population growth (annual %)
excel_url_urban = 'https://api.worldbank.org/v2/en/indicator/SP.URB.GROW?downloadformat=excel'
# The Excel URL below indicates electricity production from oil, gas, and coal sources (% of total)
excel_url_electricity = 'https://api.worldbank.org/v2/en/indicator/EG.ELC.FOSL.ZS?downloadformat=excel'

# The Excel URL below indicates Agriculture, forestry, and fishing, value added (% of GDP)
excel_url_agriculture = 'https://api.worldbank.org/v2/en/indicator/NV.AGR.TOTL.ZS?downloadformat=excel'

# The Excel URL below indicates CO2 emissions (metric tons per capita)
excel_url_CO2 = 'https://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.PC?downloadformat=excel'

# Parameters for reading and transposing data
sheet_name = 'Data'
new_cols = ['Country Name', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']
countries = ['Germany', 'United States', 'United Kingdom', 'Pakistan', 'China', 'Panama', 'Norway']

# Read and transpose arable land data
data_arable_land, data_arable_land_transpose = read_data_excel(excel_url_arable_land, sheet_name, new_cols, countries)

# Read and transpose forest area data
data_forest_area, data_forest_area_transpose = read_data_excel(excel_url_forest_area, sheet_name, new_cols, countries)

# Read and transpose GDP data
data_GDP, data_GDP_transpose = read_data_excel(excel_url_GDP, sheet_name, new_cols, countries)

# Read and transpose Urban population growth data
data_urban_read, data_urban_transpose = read_data_excel(excel_url_urban, sheet_name, new_cols, countries)

# Read and transpose electricity production data
data_electricity_read, data_electricity_transpose = read_data_excel(excel_url_electricity, sheet_name, new_cols, countries)

# Read and transpose agriculture data
data_agriculture_read, data_agriculture_transpose = read_data_excel(excel_url_agriculture, sheet_name, new_cols, countries)

# Read and transpose CO2 emissions data
data_CO2, data_CO2_transpose = read_data_excel(excel_url_CO2, sheet_name, new_cols, countries)



def line_plot(x_data, y_data, xlabel, ylabel, title, labels, colors):
    """
    Creates a line plot for multiple datasets.

    Parameters:
    - x_data (array): X-axis data.
    - y_data (array of arrays): Y-axis data for multiple datasets.
    - xlabel (str): Label for the X-axis.
    - ylabel (str): Label for the Y-axis.
    - title (str): Title of the plot.
    - labels (list): Labels for each dataset.
    - colors (list): Colors for each dataset.
    """
    plt.figure(figsize=(8, 6), dpi=200)
    plt.title(title, fontsize=7)

    for i in range(len(y_data)):
        plt.plot(x_data, y_data[i], label=labels[i], color=colors[i])

    plt.xlabel(xlabel, fontsize=7)
    plt.ylabel(ylabel, fontsize=7)
    plt.legend(bbox_to_anchor=(1.02, 1))
    plt.show()

# Print the transposed data
print(data_GDP_transpose)

# Describe the statistics of GDP growth (annual %)
GDP_statistics = data_GDP_transpose.describe()
print(GDP_statistics)

# Line plot for GDP growth (annual %)
x_data = data_GDP_transpose.index
y_data = [data_GDP_transpose['Germany'],
          data_GDP_transpose['United States'],
          data_GDP_transpose['United Kingdom'],
          data_GDP_transpose['Pakistan'],
          data_GDP_transpose['China'],
          data_GDP_transpose['Panama'],
          data_GDP_transpose['Norway']]
xlabel = 'Years'
ylabel = '(%) GDP Growth'
labels = ['Germany', 'USA', 'UK', 'Pakistan', 'China', 'Panama', 'Norway']
colors = ['purple', 'magenta', 'blue', 'green', 'yellow', 'red', 'black']
title = 'Annual (%) GDP Growth Countries'

# Line plot
line_plot(x_data, y_data, xlabel, ylabel, title, labels, colors)

# Display the transposed data
print(data_arable_land_transpose)
print(data_forest_area_transpose)

# Calculate correlation between arable land and forest area
correlation_arable_forest = data_arable_land_transpose.corrwith(data_forest_area_transpose)

# Print the correlation
print("Correlation between Arable Land and Forest Area:")
print(correlation_arable_forest)

# Line plot for years vs. arable land and forest area
line_plot(data_arable_land_transpose.index, [data_arable_land_transpose[country] for country in countries],
             'Years', 'Arable Land (% of land area)',
             'Arable Land vs. Forest Area for Countries', countries, ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'brown'])

def barplot(labels_array, width, y_data, y_label, label, title, rotation=0):
    """
    Plot a grouped bar plot.

    Parameters:
    - labels_array (array-like): X-axis labels.
    - width (float): Width of each bar group.
    - y_data (list of array-like): Y-axis data for each bar.
    - y_label (str): Y-axis label.
    - label (list): Labels for each bar group.
    - title (str): Plot title.
    - rotation (float): Rotation angle for X-axis labels.
    """
    x = np.arange(len(labels_array))
    fig, ax = plt.subplots(figsize=(8, 6), dpi=200)

    for i in range(len(y_data)):
        plt.bar(x + width * i, y_data[i], width, label=label[i])

    plt.title(title, fontsize=7)
    plt.ylabel(y_label, fontsize=7)
    plt.xlabel(None)
    plt.xticks(x + width * (len(y_data) - 1) / 2, labels_array, rotation=rotation)

    plt.legend()
    ax.tick_params(bottom=False, left=True)

    plt.show()

# Define a function to create a correlation heatmap
def correlation_heatmap(data, corr, title):
    """
    Displays a correlation heatmap for the given data.

    Parameters:
    - data (DataFrame): Input data.
    - corr (DataFrame): Correlation matrix.
    - title (str): Title for the heatmap.
    """
    plt.figure(figsize=(8, 6), dpi=200)
    plt.imshow(corr, cmap='coolwarm', interpolation='none')
    plt.colorbar()

    # Show all ticks and label them with the dataframe column name
    plt.xticks(range(len(data.columns)), data.columns, rotation=90, fontsize=7)
    plt.yticks(range(len(data.columns)), data.columns, rotation=0, fontsize=7)

    plt.title(title, fontsize=7)

    # Loop over data dimensions and create text annotations
    labels = corr.values
    for i in range(labels.shape[0]):
        for j in range(labels.shape[1]):
            plt.text(j, i, '{:.2f}'.format(labels[i, j]),
                     ha="center", va="center", color="white")

    plt.show()

# Parameters for producing grouped bar plots of Urban population growth (annual %)
labels_array_urban = ['Pakistan', 'USA', 'UK', 'Panama', 'China', 'Brazil', 'Australia']
width_urban = 0.2
y_data_urban = [data_urban_read['2019'],
                data_urban_read['2020'],
                data_urban_read['2021'],
                data_urban_read['2022']]
y_label_urban = 'Urban growth'
label_urban = ['Year 2019', 'Year 2020', 'Year 2021', 'Year 2022']
title_urban = 'Urban population growth (annual %)'

# Grouped bar plot
barplot(labels_array_urban, width_urban, y_data_urban, y_label_urban, label_urban, title_urban)

# Create a dataframe for Germany using selected indicators
data_Germany = {
    'Urban pop. growth': data_urban_transpose['Germany'],
    'Electricity production': data_electricity_transpose['Germany'],
    'Agric. forestry and Fisheries': data_agriculture_transpose['Germany'],
    'CO2 Emissions': data_CO2_transpose['Germany'],
    'Forest Area': data_forest_area_transpose['Germany'],
    'GDP Annual Growth': data_GDP_transpose['Germany']
}
df_Germany = pd.DataFrame(data_Germany)

# Display the dataframe and correlation matrix
print(df_Germany)
corr_Germany = df_Germany.corr()
print(corr_Germany)

# Display the correlation heatmap for Germany
correlation_heatmap(df_Germany, corr_Germany, 'Germany')

# Create a dataframe for Germany using selected indicators
data_Panama = {
    'Urban pop. growth': data_urban_transpose['Panama'],
    'Electricity production': data_electricity_transpose['Panama'],
    'Agric. forestry and Fisheries': data_agriculture_transpose['Panama'],
    'CO2 Emissions': data_CO2_transpose['Panama'],
    'Forest Area': data_forest_area_transpose['Panama'],
    'GDP Annual Growth': data_GDP_transpose['Panama']
}
df_Panama = pd.DataFrame(data_Panama)

# Display the dataframe and correlation matrix
print(df_Panama)
corr_Panama = df_Panama.corr()
print(corr_Panama)

# Display the correlation heatmap for Germany
correlation_heatmap(df_Panama, corr_Panama, 'Panama')

# Plot a multiple line plot for Electricity Production (annual %) for selected countries
x_data_electricity = data_electricity_transpose.index
y_data_electricity = [data_electricity_transpose[country] for country in countries]
xlabel_electricity = 'Years'
ylabel_electricity = '(%) Electricity Production'
labels_electricity = countries
colors_electricity = ['orange', 'pink', 'cyan', 'purple', 'green', 'red', 'blue', 'yellow', 'brown', 'gray', 'teal', 'magenta', 'purple', 'orange', 'blue']
title_electricity = 'Annual (%) of Electricity Production of different Countries'

# Plot the line plots for Electricity Production of selected countries
line_plot(x_data_electricity, y_data_electricity, xlabel_electricity, ylabel_electricity, title_electricity, labels_electricity, colors_electricity)


# Plot a grouped bar plot for Agriculture, forestry, and fishing, value added (% of GDP) for fifteen countries
labels_array_agr = countries
width_agr = 0.2
y_data_agr = [
    data_agriculture_read['2019'],
    data_agriculture_read['2020'],
    data_agriculture_read['2021'],
    data_agriculture_read['2022']
]
y_label_agr = '% of GDP'
label_agr = ['Year 2019', 'Year 2020', 'Year 2021', 'Year 2022']
title_agr = 'Agriculture, forestry, and fishing, value added (% of GDP) for Random Countries'

# Plot the grouped bar plot for fifteen countries
barplot(labels_array_agr, width_agr, y_data_agr, y_label_agr, label_agr, title_agr, rotation=55)
