from gsheets import Sheets
import pandas as pd

sheets = Sheets.from_files('cowin_client_secret.json', 'storage.json')
sheet_url='https://docs.google.com/spreadsheets/d/15ZQYCKIGeMYyRquLe5Ej5Kecl7KNHxTRmy-BHKDEY14/edit#gid=157750423'
d = sheets.get(sheet_url)
## Murshita  meal services.
murshitha = d.sheets[3].to_frame(usecols=range(14))
## Harshini  meal services.
harshini = d.sheets[4].to_frame()
## Food delivery Old meal services
# df = d.sheets[5].to_frame()

def get_clean_contact_info(df,col_name):
    """
    Function to clean contact info field
    df : Dataframe
    col_name : Column name specifying contact info field
    """
    ## remove na
    df = df[~df[col_name].isna()]
    ## Convert to string
    df[col_name] = df[col_name].astype('str')
    ## get rid of spaces
    df[col_name] = df[col_name].str.replace(' ','')
    ##return dataframe
    return df

## Drop rows where contact info is null
murshitha = get_clean_contact_info(murshitha,'Mobile \nNumber')
harshini = get_clean_contact_info(harshini,'Contact Number')

def concatenate_column_values_to_comments_section(df,col_names,fill_na='No Value present'):
    """
    Function to concatenate extra columns into a single 'Comments' column
    df : DataFrame
    col_names: :List of column names in specifc order to be concatenated
    fill_na:Default fill na values
    """
    for idx,val in enumerate(col_names):
        if idx == 0:
            df['Comments'] = val + ' : ' + df[val].fillna(fill_na) + ';\n'
        else:
            df['Comments'] += val + ' : ' + df[val].fillna(fill_na) + ';\n'
    return df

def treat_duplicates(df,ph_no_col_name,check_unique_col_names):
    duplicated_phone_numbers = df[ph_no_col_name][df[ph_no_col_name].duplicated()]
    for number in duplicated_phone_numbers:
        temp = df[df['Phone Number'] == number].fillna('No Value Present')
        rows = {}
        for col in check_unique_col_names:
            unique = ','.join(temp[col].str.strip().unique())
#             df.loc[(df['Phone Number'] == number).index][col] = unique
            temp[col] = unique
        df[df['Phone Number'] == number] = temp
    return df.drop_duplicates(subset=check_unique_col_names)

def treat_duplicates(df,ph_no_col_name,check_unique_col_names):
    """
    Function to treat duplicates.
    :param df: Dataframe
    :param ph_no_col_name: Name of column containing Phone numbers.
    :param check_unique_col_names: List of columns to be checked for consolidation of row values into single row in case of duplicates.
    :return:
    """
    duplicated_phone_numbers = df[ph_no_col_name][df[ph_no_col_name].duplicated()]
    for number in duplicated_phone_numbers:
        temp = df[df['Phone Number'] == number].fillna('No Value Present')
        for col in check_unique_col_names:
            unique = ','.join(temp[col].str.strip().unique())
            temp[col] = unique
        df[df['Phone Number'] == number] = temp
    return df.drop_duplicates(subset=check_unique_col_names)


## Standardize to meals format
target_columns = ['Name','Address','Latitude','Longitude','Phone Number','Type','Free','Comments','Cost Type']

#################### Harshini - Start
## Rename columns in Harshini to columns in target columns
harshini = harshini.rename({'Prepared By':'Name','Contact Number':'Phone Number'},axis=1)
harshini=treat_duplicates(harshini,'Phone Number',['Phone Number','Area', 'Order Placement', 'Delivery Option',
       'Delivery Time', 'Delivered by', 'Notes', 'Max order that can be placed'])
harshini = concatenate_column_values_to_comments_section(harshini,['Area', 'Order Placement', 'Delivery Option',
       'Delivery Time', 'Delivered by', 'Notes', 'Max order that can be placed'])
## Insert empty columns at respective positions
harshini = harshini.reindex(columns=target_columns)
#################### Harshini - Complete

#################### murshitha - Start
murshitha['Name'] += '\nContact Name: ' + murshitha['Contact Name'].fillna('No Value Present')

## Rename columns in Harshini to columns in target columns
murshitha = murshitha.rename({'Meal Type':'Type','Mobile \nNumber':'Phone Number'},axis=1)
murshitha = treat_duplicates(murshitha,'Phone Number',['Phone Number','Location of Kitchen', 'Delivery Mode', 'Any other details you would like to share?',
       'Do you offer Covid Specific Diet food?', 'Would you consider donating some meals to those who are isolated but unable to afford to order meals?'
        ,'Verified'])
murshitha = concatenate_column_values_to_comments_section(murshitha,['Location of Kitchen', 'Delivery Mode', 'Any other details you would like to share?',
       'Do you offer Covid Specific Diet food?', 'Would you consider donating some meals to those who are isolated but unable to afford to order meals?'
        ,'Verified' ])
## Insert empty columns at respective positions
murshitha = murshitha.reindex(columns=target_columns)
#################### murshitha - Complete



meals_df = pd.concat([harshini,murshitha])
final_meals_df = treat_duplicates(meals_df,'Phone Number',[ 'Phone Number','Type','Comments']).fillna('No Value Present')

## Store dataframe
final_meals_df.to_csv('tamil_nadu_meals.csv',index=False)