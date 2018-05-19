import pandas as pd
import numpy as np
import re

def answer_one():
    FILE1 = 'Energy Indicators.xls'
    column_names = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy = pd.read_excel(FILE1, skip_footer=38, skiprows=16, header=1, usecols=[2,3,4,5], names=column_names)
    energy['Energy Supply'] = energy.apply(lambda x: np.NaN if x['Energy Supply'] == '...' else x['Energy Supply'], axis=1)
    energy['Energy Supply per Capita'] = energy.apply(lambda x: np.NaN if x['Energy Supply per Capita'] == '...' else x['Energy Supply per Capita'], axis=1)
    energy['Energy Supply'] = energy['Energy Supply']*1000

    def fix_country_name(name):
        try:
            name = re.match(r'([a-zA-Z, ]*)[0-9|\(].*', name['Country'])[1]
            if name[-1] == ' ':
                name = name[0:-1]
            return name
        except:
            return name
    energy['Country'] = energy.apply(fix_country_name, axis=1)

    rename_country = {
        "Republic of Korea": "South Korea",
        "United States of America": "United States",
        "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
        "China, Hong Kong Special Administrative Region": "Hong Kong"
    }

    for k, v in rename_country.items():
        energy['Country'][energy[energy['Country'] == k].index] = str(v)
        #energy.iloc[energy[energy['Country'] == k].index]['Country'] = str(v)
        #energy[energy['Country'] == k]['Country'] = "teste"
    #energy['Country'][30:50]

    FILE2 = 'world_bank.csv'
    GDP = pd.read_csv(FILE2, skiprows=4)
    year_range = ["Country Name"] + list(str(i) for i in range(2006,2016))
    GDP = GDP[year_range]
    rename_country = {
        "Korea, Rep.": "South Korea", 
        "Iran, Islamic Rep.": "Iran",
        "Hong Kong SAR, China": "Hong Kong"
    }
    for k, v in rename_country.items():
        GDP["Country Name"][GDP[GDP["Country Name"] == k].index] = str(v)

    FILE3 = 'scimagojr-3.xlsx'
    ScimEn = pd.read_excel(FILE3)
    ScimEn = ScimEn[(ScimEn['Rank'] > 0) & (ScimEn['Rank'] <= 15)]

    merged = GDP.merge(ScimEn, how='inner', left_on='Country Name', right_on='Country').merge(energy, how='inner', on='Country').copy()
    #df = ScimEn.merge(energy, how='inner', on='Country').merge(GDP, how='inner', left_on='Country', right_on='Country Name')
    del merged['Country Name']
    merged = merged.set_index('Country')
    return merged.copy()
