# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# embed streamlit docs in a streamlit app
# components.iframe("https://www.baidu.com")

pr_1 = pd.read_csv("pr_1.csv")
print(pr_1)

pop_routes_origin_dict = {"NOC": 'Ireland West Knock Airport, Ireland',
                          "TGD": 'Podgorica Airport, Montenegro',
                          "KWA": 'Bucholz Army Air Field, Marshall Islands',
                          "CGH": 'Congonhas Airport, Brazil', "CKH": 'Chokurdakh Airport, Russia',
                          "HDF": 'Heringsdorf Airport, Germany', "OND": 'Ondangwa Airport, Namibia',
                          "XMH": 'Manihi Airport', "LUA": 'Lukla Airport, Nepal',
                          "AKX": 'Aktobe Airport, Kazakhstan'}
pop_routes_dest_dict = {"LGW": 'London Gatwick Airport, United Kingdom, London',
                        "BEG": 'Belgrade Nikola Tesla Airport, Serbia',
                        "MAJ": 'Marshall Islands International Airport',
                        "SDU": 'Santos Dumont Airport, Brazil', "YKS": 'Yakutsk Airport, Russia',
                        "LUX": 'Luxembourg-Findel International Airport, Luxembourg',
                        "ERS": 'Eros Airport, Namibia',
                        "PPT": 'Faa International Airport, French Polynesia',
                        "KTM": 'Tribhuvan International Airport, Nepal',
                        "ALA": 'Almaty Airport, Kazakhstan'}

pr_1.replace({'ORIGIN': pop_routes_origin_dict}, inplace = True)
# , 'DESTINATION': pop_routes_dest_dict},
print(pr_1)
