import pandas as pd
df = pd.read_csv('/Users/shamlaaqthariit/Desktop/Desktop - Shamla’s MacBook Pro/IIT /w2149479_Disaster_Displacement_Dashboard/Raw Dataset/internal-displacements-new-displacements-associated-with-disasters.csv')
###
#Removing duplicated rows
df = df.drop_duplicates()
#Dropping columns with majority of null values and unneccesary information
drop_cols = ['hazard_subtype_name',
              'total_displacement', 
              'total_displacement_rounded',
              'start_date_accuracy',
              'end_date_accuracy',
              'event_codes']
df_clean = df.drop(columns=drop_cols)
###
#droping rows with no country name (14)
df_clean = df_clean.dropna(subset=['country_name'])
###
#Date conversions
df_clean['start_date'] = pd.to_datetime(df_clean['start_date'])
df_clean['end_date'] = pd.to_datetime(df_clean['end_date'])
###
#saving the clean ver of the dataset
df_clean.to_csv('cleaned_data.csv',index=False)

#cleaned df test
print('Cleaned dataset')
print('\nFirst Five Rows')
print(df_clean.head())
print('\nMissing values check')
print(df_clean.isnull().sum())
print('\nDuplicate rows check')
print(df_clean.duplicated().sum())



