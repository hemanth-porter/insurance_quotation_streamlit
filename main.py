from classified import VehicleQuote
from constants import *
import pandas as pd
import streamlit as st
import traceback
import sys

sys.path.append("data/")

commission_df = pd.read_excel(price_deets_file_name,sheet_name = commission_sheet)
rtos_df = pd.read_excel(price_deets_file_name,sheet_name = rtos_sheet)
rates_df = pd.read_excel(price_deets_file_name,sheet_name = rates_sheet)
vaahan_data = pd.read_excel(vaahan_file_name)



# ## Fixing Typo Errors

commission_df.loc[commission_df["City"] == "Rest of Telengana", "City"] = "Rest of Telangana"

vehicle_number = st.text_input("Enter the vehicle number:", max_chars=10)
# vehicle_number = "TS13UC6498"

# for vehicle_number in list(vaahan_data[vaahan_data[manf_year_col].notna()]["registration_number"][20:40]):
if vehicle_number:
    st.write(vehicle_number)

    try:

        vn1 = VehicleQuote(vehicle_number, commission_df, rtos_df, rates_df, vaahan_data)

        results, log_results = vn1.get_quote()

        st.write(results)

        st.write(log_results)

    except Exception as e:
        st.write("Error occured")
        st.write(traceback.format_exc())
        st.write()

# ## QC

pd.set_option('display.max_columns', None)

print("Sample Vehicle Numbers for testing: ","TS13UC4513","TS07UL1462","TS13UC6498","TS07UK1169","TS07UK2562","TS07UK2505")

# commission_df #TS13UC4513 Sample 



# vaahan_data.iloc[12935]

# +
# display(vaahan_data[vaahan_data['registration_number'] == 'TS07UK1169'])

# +
# string_list = [x for x in list(commission_df["Payout"].unique()) if isinstance(x, str)]

# +
# vaahan_data[vaahan_data[manf_year_col].notna()]["registration_number"] == TS08UE9075

# +
# vaahan_data[vaahan_data.registration_number == 'TS08UE9075']

# +

#   # Print the exception
#   print(traceback.format_exc())

# +
# def is_substring(string, list_of_strings):
#     for s in list_of_strings:
#         if string in s:
#             return True
#     return False

# l = list(commission_df['Vehicle Company'].unique())

# is_substring("TAT", )

# filtered_list = [s for s in l if not pd.isnull(s)]

# filtered_list

# +
# city_names_list = commission_df.City.unique()
# city_names_list = [s for s in city_names_list if not pd.isnull(s)]
# lowercase_city_strings = [s.lower() for s in city_names_list]

# +
# is_substring("rest of telangana".lower(), lowercase_city_strings)
# -


