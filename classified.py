import pandas as pd
import pip
import streamlit as st
pip.main(["install", "openpyxl"])
from constants import *

# +
class VehicleQuote:
    def __init__(self, vehicle_number, commission_df, rtos_df, rates_df, vaahan_data):
        self.vehicle_number = vehicle_number
        self.commission_df = commission_df
        self.rtos_df = rtos_df
        self.rates_df = rates_df
        self.vaahan_data = vaahan_data
        self.return_output = True


    def get_rto(self):
        rto = self.vehicle_number[:4].upper()
        if rto in list(self.rtos_df['RTO List']):
            rto = rto
        else:
            rto = rto[:2]

        return rto
        
    def clean_gvw(self, gvw_range):
        """
        Cleans the GVW column 
        """
        if gvw_range == "0-2500":
            return "0-2500"
        elif gvw_range == "0 to 2500":
            return "0-2500"
        elif gvw_range == "0-3500":
            return "0-3500"

    def get_gvw_range(self, gvw):
        if gvw <= 2500:
            return "0-2500"
        elif gvw <= 3500: 
            return "0-3500"

    def get_vehicle_details(self):
        rto = self.get_rto()
        vehicle_city = self.rtos_df[self.rtos_df['RTO List'] == rto]['City'].iloc[0]

        my_vehicle_data = self.vaahan_data[self.vaahan_data[vehicle_number_col] == self.vehicle_number]

        mnf_year = my_vehicle_data[manf_year_col].iloc[0].year
        raw_vehicle_company = my_vehicle_data[vehicle_company_col].iloc[0]
        vehicle_company_cleaned = my_vehicle_data["vehicle_company_cleaned"].iloc[0]
        gvw = my_vehicle_data[gvw_col].iloc[0]

        gvw_range = self.get_gvw_range(gvw)

        return vehicle_city, mnf_year, raw_vehicle_company, vehicle_company_cleaned, gvw_range

    
    def clean_commission_df(self, commission_df):
        for each_col in list(commission_df.columns):
            commission_df[each_col] = commission_df[each_col].apply(lambda x: str(x).strip())

        commission_df['GVW'] = commission_df['GVW'].apply(lambda x: self.clean_gvw(x))

        return commission_df

    
    def get_company_name(self, company_name_row):
        try:
            if "MAHINDRA".lower() in company_name_row.lower():
                return "MAHINDRA".lower()
            elif "TATA".lower() in company_name_row.lower():
                return "TATA".lower()
            elif "Maruti".lower() in company_name_row.lower():
                return "Maruti".lower()
            elif "Ashok leyland".lower() in company_name_row.lower():
                return "Ashok leyland".lower()
            elif "Bajaj".lower() in company_name_row.lower():
                return "Bajaj".lower()
            # User input for this case but print current name, for the user to enter a company name.
            else:  # Should be a dropdown form the possible filtered list
                return "Company name not readable, please enter"
        except:
            return "Error in fetching company name"  # User input for this case
        
    def get_vehcile_company_list(self,vehicle_company_cleaned):
        if vehicle_company_cleaned.lower() == 'MAHINDRA'.lower():
            return_list = ["MAHINDRA", "Except TATA and Maruti", "ALL"]
        elif vehicle_company_cleaned.lower() == 'TATA'.lower():
            return_list = ["TATA","TATA and Maruti", "Except Mahindra", "ALL"]
        elif vehicle_company_cleaned.lower() == 'Maruti'.lower():
            return_list = ["Maruti","TATA and Maruti", "Except Mahindra", "ALL"]
        elif vehicle_company_cleaned.lower() == 'Ashok leyland'.lower():
            return_list = ["Ashok leyland","Except TATA and Maruti", "Except Mahindra", "ALL"]
        else:
            return_list = ["Except TATA and Maruti", "Except Mahindra", "ALL"]

        return_list = list(map(str.lower, return_list))

        return return_list
    
    @staticmethod
    def is_substring(string, list_of_strings):
        for s in list_of_strings:
            if string in s:
                return True
        return False
    


    def get_quote(self):

        log = []
        
        self.vaahan_data["vehicle_company_cleaned"] = self.vaahan_data[vehicle_company_col].apply(lambda x : self.get_company_name(x))

        city, mnf_year, vehicle_company, vehicle_company_cleaned, gvw_range = self.get_vehicle_details()
        
        city_names_list = self.commission_df.City.unique()
        city_names_list = [s for s in city_names_list if not pd.isnull(s)]
        lowercase_city_strings = [s.lower() for s in city_names_list]
        
        log.append(f"Name of the city : {city}")
        log.append(f"Name of the company: {vehicle_company}")
        
        

#         if self.is_substring(city.lower(), lowercase_city_strings):  # City of the chosen vehicle is present in the commission_sheet
#             pass
#         else:
#             log.append(f"{city.lower()} City not present in commission_sheet")

        # If the vehicle is 2021 and 2022 make and model, and >2.5T request for quotation.
        if mnf_year == 2021 or mnf_year == 2022:
            if gvw_range != "0-2500":  # >2.5T
                log.append(f"{vehicle_company} vehicles of this make and model are not insured by us")

        # If the vehicle is >2.5T
        if gvw_range != "0-2500":
            log.append(f"{vehicle_company} vehicles above 2.5T are not insured by us")
            self.return_output = False
            return st.write("Vehicles above 2.5T are not insured by us"), log

        
        company_names_list = self.commission_df['Vehicle Company'].unique()
        company_names_list = [s for s in company_names_list if not pd.isnull(s)]
        lowercase_company_strings = [s.lower() for s in company_names_list]
        
        
#         if self.is_substring(vehicle_company_cleaned.lower(), lowercase_company_strings):  # Company of the chosen vehicle is present in the commission_sheet
#             pass
#         else:
#             log.append(f"{vehicle_company} not present in commission_sheet")
#             log.append(f"{vehicle_company_cleaned} is the cleaned company name")

        #To remove any blank spaces at the end or start
        commission_df = self.clean_commission_df(self.commission_df) 

        if vehicle_company_cleaned == 'Company name not readable, please enter':
            st.write(vehicle_company)
            # vehicle_company_cleaned = input("Enter: ",)            
            vehicle_company_cleaned_input = st.text_input("Enter company name:")
            if vehicle_company_cleaned_input:
                vehicle_company_cleaned = vehicle_company_cleaned_input
                self.return_output = True
            else:
                self.return_output = False
                return st.write("Please type the name of the vehicle company"), log
            
        #Gettign the commission df only for the city of the chosen vehicle and the GVW
        commission_df_city_gvw_filtered = commission_df[
                            ( commission_df['City'].apply(lambda x: x.lower()) == city.lower() ) & 
                            ( commission_df['GVW'] == gvw_range )]

        avaiable_company_list = list(commission_df_city_gvw_filtered["Vehicle Company"].unique())

        vehcile_company_list = self.get_vehcile_company_list(vehicle_company_cleaned)

        #Gettign the commission df only for the Company of the chosen vehicle
        commission_df_company_filtered = commission_df_city_gvw_filtered[
            commission_df_city_gvw_filtered["Vehicle Company"].apply(lambda x: x.lower()).isin(vehcile_company_list)]
        
        commission_df_company_filtered['Payout'] = commission_df_company_filtered['Payout'].astype(float)


        final_df = commission_df_company_filtered.sort_values(by = "Payout", ascending = False)
        
        if self.return_output == True:
            return final_df,log
