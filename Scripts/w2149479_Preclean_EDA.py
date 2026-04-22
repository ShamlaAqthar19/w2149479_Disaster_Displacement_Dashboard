import pandas as pd
#dataset loading
df = pd.read_csv('Raw Dataset/internal-displacements-new-displacements-associated-with-disasters.csv')
#Basic overview
print('First five rows')
print(df.head())
print('\nNumber of rows and columns')
print(df.shape)
print('\nData Types')
print(df.dtypes)
print('Country name check')
print(df['country_name'].unique())
#missing values
print('\nMissing values')
print(df.isnull().sum())
#duplicate rows
print('\nDuplicate rows')
print(df.duplicated().sum())
#hazard types
print('\nHazard types')
print(df['hazard_type_name'].value_counts())
#summary statistics
print('\nSummary statistics')
print(df['new_displacement'].describe())
#checking if all years have displacement
print('\nDisplacement by year')
print(df.groupby('year')['new_displacement'].sum())
#checking for displacements based on each hazrad cat
print('\nDisplacement by hazard category')
print(df.groupby('hazard_category_name')['new_displacement'].sum())
#checking for displacements based on the event
print('\nDisplacement by hazard type')
print(df.groupby('hazard_type_name')['new_displacement'].sum())