import requests
import streamlit as st
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie
from PIL import Image
import pandas as pd
import snowflake.connector
import os

# Define connection parameters

conn = snowflake.connector.connect(user='jedi1', password='Jedi1234!', account='ur88629.ap-southeast-2',
                                   warehouse='Emission',
                                   database='MARKETPLACE_EMISSIONS', schema='PROOF_OF_CONCEPT')

# Set page config
st.set_page_config(page_title="EcoFly", page_icon=":airplane:", layout="wide")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Use local CSS
# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#
# local_css("C:/Users/adrane/PycharmProjects/Snowflake_Streamlit/style.css")

# ---- LOAD ASSETS ----
lottie_emission = load_lottieurl("https://assets1.lottiefiles.com/private_files/lf30_dy2xdidy.json")
lottie_emission_1 = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_bknkrt5y.json")
lottie_burn = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_ZhtOc0.json")
lottie_airport = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_jlmgqgx2.json")
lottie_worst_fl = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_vyixuzos.json")
lottie_avoid = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_ymjrns2k.json")
lottie_fuel_burn = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_no9qrf5p.json")
lottie_CO2 = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_wst709y2.json")
lottie_cust = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_EHugAD.json")
# img_contact_form = Image.open("images/yt_contact_form.png")
# img_lottie_animation = Image.open("images/yt_lottie_animation.png")


# ---- Container for header ----
with st.container():
    left_column, inter_cols_pace, right_column = st.columns((2, 8, 2))
    with left_column:
        st.title("EcoFly")
        st.subheader("by Deloitte")
        # st.title("")
        st.write(
            "We are passionate about finding ways to shrink carbon footprint in the air."
        )
        st.write(
            "Check out our carbon emission analysis before booking your flights."
        )
    with right_column:
        deloitte_img = 'https://raw.githubusercontent.com/lazycoder181/eco-fly/master/de.jpg'
        st.image(deloitte_img)

# Defining different tabs
tab1, tab2, tab3, best_flights_tab, worst_flights_tab, avoid_flights_tab, fuel_burn_tab, CO2_tab, cust_tab = st.tabs([
    "SkyScanner",
    "Greenhouse Impact", "Busiest Airports for Departures", "Top 5 flights", "Non-Eco-friendly Flights",
    "Flights to Avoid", "Fuel Burn", 'CO2 Emission', 'Best Flights for Customers'])
# tab4

with tab1:
    # st.header(
    # components.iframe(
    #     "https://www.skyscanner.com.au/?&utm_source=google&utm_medium=cpc&utm_campaign=AU-Travel-Search-Brand-Skyscanner-Exact&utm_term=skyscanner&associateID=SEM_GGT_19370_00045&gclid=CjwKCAjwhNWZBhB_EiwAPzlhNoRMkbbkv5gyoFROA8t3Wo0MaIX7kjk6KesPuVDZefyX3r8Ww0Y6PxoCmmkQAvD_BwE&gclsrc=aw.ds)")
    image = 'https://raw.githubusercontent.com/lazycoder181/eco-fly/master/skyscanner.PNG'
    st.image(image, caption='Skyscanner', width=1750)
    st.write(
        "[Book here>](https://www.skyscanner.com.au/transport/flights-from/mela/221005/221012/?adults=1&adultsv2=1&cabinclass=economy&children=0&childrenv2=&inboundaltsenabled=false&infants=0&originentityid=27544894&outboundaltsenabled=false&preferdirects=false&ref=home&rtn=1)")

with tab2:
    # st.header("Greenhouse Impact")
    # ---- Container for Total Co2 emission----
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            # For years 2021-2022
            st.subheader("Total Co2 emission in 2021-2022")
            total_emission_latest = pd.read_sql(
                f"SELECT AIRLINECODE, SUM(ESTIMATED_CO2_EMISSIONS_TONNES) AS TOTAL_CO2_EMISSION FROM SCHEDULED_FLIGHT_EMISSIONS GROUP BY AIRLINECODE ORDER BY SUM(ESTIMATED_FUEL_BURN_TONNES) DESC LIMIT 10",
                conn)
            total_emission_latest = total_emission_latest.set_index(['AIRLINECODE'])
            st.bar_chart(total_emission_latest)
        with right_column:
            # For year 2019
            st.subheader("Total Co2 emission in 2019")
            total_emission_hist = pd.read_sql(
                f"SELECT AIRLINECODE, SUM(ESTIMATED_CO2_EMISSIONS_TONNES) AS TOTAL_CO2_EMISSION FROM FLIGHTS2019 GROUP BY AIRLINECODE ORDER BY SUM(ESTIMATED_FUEL_BURN_TONNES) DESC LIMIT 10",
                conn)
            total_emission_hist = total_emission_hist.set_index(['AIRLINECODE'])

            st.bar_chart(total_emission_hist)

    # ---- Container for Total Fuel burn----

    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        # For years 2021-2022
        with left_column:
            st.subheader("Total Fuel burn in 2021-2022 based on Airlines ")

            total_burn_latest = pd.read_sql(
                f"SELECT AIRLINECODE, SUM(ESTIMATED_FUEL_BURN_TONNES) AS TOTAL_FUEL_BURN FROM SCHEDULED_FLIGHT_EMISSIONS GROUP BY AIRLINECODE ORDER BY SUM(ESTIMATED_CO2_EMISSIONS_TONNES) DESC LIMIT 10;",
                conn)
            total_burn_latest = total_burn_latest.set_index(['AIRLINECODE'])
            st.bar_chart(total_burn_latest)
        # For year 2020
        with right_column:
            st.subheader("Total Fuel burn in 2019 based on Airlines")

            total_burn_hist = pd.read_sql(
                f"SELECT AIRLINECODE, SUM(ESTIMATED_FUEL_BURN_TONNES) AS TOTAL_FUEL_BURN FROM FLIGHTS2019 GROUP BY AIRLINECODE ORDER BY SUM(ESTIMATED_CO2_EMISSIONS_TONNES) DESC LIMIT 10;",
                conn)
            total_burn_hist = total_burn_hist.set_index(['AIRLINECODE'])
            st.bar_chart(total_burn_hist)

        st.write(
            "[Check out how carbon emission effects us>](https://www.dcceew.gov.au/climate-change/policy/climate-science/understanding-climate-change)")

with tab3:
    # st.header("Busiest Airports for Departures")
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("Busiest Airports")

            pop_air = pd.read_sql(
                f"SELECT TOP 10 DEPARTURE_AIRPORT, COUNT(*) AS flight_count FROM SCHEDULED_FLIGHT_EMISSIONS WHERE CAST(SCHEDULED_DEPARTURE_DATE AS DATE) >= CAST('2021-08-27' AS DATE) AND CAST(SCHEDULED_DEPARTURE_DATE AS DATE) < CAST('2022-08-27' AS DATE) GROUP BY 1 ORDER BY 2 DESC;",
                conn)

            pop_air = pop_air.set_index(['DEPARTURE_AIRPORT'])
            st.line_chart(pop_air)

        with right_column:
            st_lottie(lottie_airport, height=300, key="airport")

with best_flights_tab:
    # st.header("Popular Routes")
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("Top 5 Flights in terms of CO2 Efficiency")

            best_flights = pd.read_sql(
                f"SELECT AIRLINECODE,FLIGHTNUMBER ,MAX(ESTIMATED_C02_EFFICIENCY) MAX_ESTIMATED_CO2_EFFICIENCY FROM(SELECT AIRLINECODE,FLIGHTNUMBER,SCHEDULED_DEPARTURE_DATE, ESTIMATED_CO2_EMISSIONS_TONNES/ESTIMATED_FUEL_BURN_TONNES as ESTIMATED_C02_EFFICIENCY,DENSE_RANK() OVER (ORDER BY ESTIMATED_C02_EFFICIENCY DESC)my_dense_rank FROM SCHEDULED_FLIGHT_EMISSIONS WHERE (ESTIMATED_FUEL_BURN_TONNES) <> 0) table1 GROUP BY AIRLINECODE,FLIGHTNUMBER ORDER BY MAX_ESTIMATED_CO2_EFFICIENCY asc LIMIT 5;",
                conn)
            best_flights = pd.DataFrame(best_flights)
            best_flights_dict = {"VS": 'Virgin Atlantic', "NH": 'All Nippon Airways Co., Ltd',
                                 "DL": 'Delta Air Lines, Inc.', "AC": 'Air Canada'}
            best_flights.replace({'AIRLINECODE': best_flights_dict}, inplace=True)
            st.dataframe(best_flights)
        with right_column:
            st_lottie(lottie_emission, height=300, key="coding")

    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            best_flights_bar = pd.read_sql(
                f"SELECT AIRLINECODE,MAX(ESTIMATED_C02_EFFICIENCY) MAX_ESTIMATED_CO2_EFFICIENCY FROM(SELECT AIRLINECODE,FLIGHTNUMBER,SCHEDULED_DEPARTURE_DATE, ESTIMATED_CO2_EMISSIONS_TONNES/ESTIMATED_FUEL_BURN_TONNES as ESTIMATED_C02_EFFICIENCY,DENSE_RANK() OVER (ORDER BY ESTIMATED_C02_EFFICIENCY DESC)my_dense_rank FROM SCHEDULED_FLIGHT_EMISSIONS WHERE (ESTIMATED_FUEL_BURN_TONNES) <> 0) table1 GROUP BY AIRLINECODE,FLIGHTNUMBER ORDER BY MAX_ESTIMATED_CO2_EFFICIENCY asc LIMIT 5;",
                conn)
            best_flights_bar.replace({'AIRLINECODE': best_flights_dict}, inplace=True)
            best_flights_bar = best_flights_bar.set_index(['AIRLINECODE'])
            st.bar_chart(best_flights_bar)
        with right_column:
            st_lottie(lottie_emission_1, height=300, key="emission_1")

with worst_flights_tab:
    # st.header("Popular Routes")
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("Top 5 Non-Eco-friendly flights")

            worst_flights = pd.read_sql(
                f"SELECT AIRLINECODE,FLIGHTNUMBER, MAX(ESTIMATED_C02_EFFICIENCY) MAX_ESTIMATED_CO2_EFFICIENCY FROM(SELECT AIRLINECODE,FLIGHTNUMBER,SCHEDULED_DEPARTURE_DATE, ESTIMATED_CO2_EMISSIONS_TONNES/ESTIMATED_FUEL_BURN_TONNES as ESTIMATED_C02_EFFICIENCY,DENSE_RANK() OVER (ORDER BY ESTIMATED_C02_EFFICIENCY DESC)my_dense_rank FROM SCHEDULED_FLIGHT_EMISSIONS WHERE (ESTIMATED_FUEL_BURN_TONNES) <> 0) table1 GROUP BY AIRLINECODE,FLIGHTNUMBER ORDER BY MAX_ESTIMATED_CO2_EFFICIENCY desc LIMIT 5 ",
                conn)
            worst_flights = pd.DataFrame(worst_flights)
            worst_flights_dict = {'OZ': 'Asiana Airlines', 'GR': 'Aurigny Airlines', "UA": 'United Airlines',
                                  "NH": 'All Nippon Airways Co., Ltd.', "MH": 'Malaysian Airlines Berhad','RVP':'Sevenair Air Services'}
            worst_flights.replace({'AIRLINECODE': worst_flights_dict}, inplace = True)
            # worst_flights = worst_flights.set_index(['AIRLINECODE'])
            st.dataframe(worst_flights)
        with right_column:
            st_lottie(lottie_worst_fl, height=300, key="worst_fl")

with avoid_flights_tab:
    # st.header("Popular Routes")
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("Flights to avoid if you are a customer")

            avoid_flights = pd.read_sql(
                f"SELECT AIRLINECODE,MAX(CARBON_OFFSET_FEE_PER_CUSTOMER) as MAX_CARBON_OFFSET_FEE_PER_CUSTOMER FROM(SELECT  AIRLINECODE, FLIGHTNUMBER,SCHEDULED_DEPARTURE_DATE, ESTIMATED_CO2_EMISSIONS_TONNES, SEATS, (ESTIMATED_CO2_EMISSIONS_TONNES *10.50) / SEATS as CARBON_OFFSET_FEE_PER_CUSTOMER FROM SCHEDULED_FLIGHT_EMISSIONS WHERE SEATS <> 0) GROUP BY AIRLINECODE, FLIGHTNUMBER ORDER BY MAX_CARBON_OFFSET_FEE_PER_CUSTOMER desc LIMIT 10;",
                conn)
            avoid_flights = pd.DataFrame(avoid_flights)
            a_f_dict = {"3S": "AeroLogic", "CA": "Air China"}
            avoid_flights.replace({'AIRLINECODE': a_f_dict}, inplace=True)
            avoid_flights = avoid_flights.set_index(['AIRLINECODE'])
            st.bar_chart(avoid_flights)
        with right_column:
            st_lottie(lottie_avoid, height=300, key="avoid")

        st.write(
            "[Airport Codes>](https://www.world-airport-codes.com/alphabetical/airport-code/a.html?page=1)")

with fuel_burn_tab:
    # st.header("Popular Routes")
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("Fuel Burn in Tonnes per AIRLINE CODE")

            fuel_burn = pd.read_sql(
                f"SELECT AIRLINECODE, SUM(ESTIMATED_FUEL_BURN_TONNES) as TOTAL_FUEL_BURNED_IN_TONNES FROM SCHEDULED_FLIGHT_EMISSIONS GROUP BY AIRLINECODE ORDER BY TOTAL_FUEL_BURNED_IN_TONNES DESC;",
                conn)
            fuel_burn = pd.DataFrame(fuel_burn)
            fuel_burn = fuel_burn.set_index(['AIRLINECODE'])
            st.bar_chart(fuel_burn)
        with right_column:
            st_lottie(lottie_fuel_burn, height=300, key="fuel_burn")
        st.write(
            "[Airport Codes>](https://www.world-airport-codes.com/alphabetical/airport-code/a.html?page=1)")

with CO2_tab:
    # st.header("Popular Routes")
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("Co2 Emission per AIRLINE CODE")

            CO2_em = pd.read_sql(
                f"SELECT AIRLINECODE, SUM(ESTIMATED_CO2_EMISSIONS_TONNES) as TOTAL_CO2_EMISSIONS_IN_TONNES FROM SCHEDULED_FLIGHT_EMISSIONS GROUP BY AIRLINECODE ORDER BY TOTAL_CO2_EMISSIONS_IN_TONNES DESC;",
                conn)
            CO2_em = pd.DataFrame(CO2_em)
            CO2_em = CO2_em.set_index(['AIRLINECODE'])
            st.bar_chart(CO2_em)
        with right_column:
            st_lottie(lottie_CO2, height=300, key="CO2")
        st.write(
            "[Airport Codes>](https://www.world-airport-codes.com/alphabetical/airport-code/a.html?page=1)")

with cust_tab:
    # st.header("Popular Routes")
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("Best flights for customers")

            cust = pd.read_sql(
                f"SELECT AIRLINECODE, MAX(CARBON_OFFSET_FEE_PER_CUSTOMER) as MIN_CARBON_OFFSET_FEE_PER_CUSTOMER FROM(SELECT  AIRLINECODE, FLIGHTNUMBER, ESTIMATED_CO2_EMISSIONS_TONNES, SEATS, ((ESTIMATED_CO2_EMISSIONS_TONNES *10.50) / SEATS) as CARBON_OFFSET_FEE_PER_CUSTOMER FROM SCHEDULED_FLIGHT_EMISSIONS WHERE SEATS <> 0) GROUP BY AIRLINECODE, FLIGHTNUMBER ORDER BY MIN_CARBON_OFFSET_FEE_PER_CUSTOMER ASC;",
                conn)
            cust = pd.DataFrame(cust)
            cust = cust.set_index(['AIRLINECODE'])
            st.bar_chart(cust)
        with right_column:
            st_lottie(lottie_cust, height=300, key="cust")
        st.write(
            "[Airport Codes>](https://www.world-airport-codes.com/alphabetical/airport-code/a.html?page=1)")
