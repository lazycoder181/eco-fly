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
lottie_burn = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_ZhtOc0.json")
lottie_airport = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_jlmgqgx2.json")
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
tab1, tab2, tab3, tab4 = st.tabs([
    "SkyScanner",
    "Greenhouse Impact", "Busiest Airports for Departures", "Popular Routes"])

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
            # Query for total fuel burn across airlines
            total_burn_latest = pd.read_sql(
                f"SELECT AIRLINECODE, SUM(ESTIMATED_FUEL_BURN_TONNES) AS TOTAL_FUEL_BURN FROM SCHEDULED_FLIGHT_EMISSIONS GROUP BY AIRLINECODE ORDER BY SUM(ESTIMATED_CO2_EMISSIONS_TONNES) DESC LIMIT 10;",
                conn)
            total_burn_latest = total_burn_latest.set_index(['AIRLINECODE'])
            st.bar_chart(total_burn_latest)
        # For year 2020
        with right_column:
            st.subheader("Total Fuel burn in 2019 based on Airlines")
            # Query for total fuel burn across airlines
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
            # Query for average fuel burn across airlines
            pop_air = pd.read_sql(
                f"SELECT TOP 10 DEPARTURE_AIRPORT, COUNT(*) AS flight_count FROM SCHEDULED_FLIGHT_EMISSIONS WHERE CAST(SCHEDULED_DEPARTURE_DATE AS DATE) >= CAST('2021-08-27' AS DATE) AND CAST(SCHEDULED_DEPARTURE_DATE AS DATE) < CAST('2022-08-27' AS DATE) GROUP BY 1 ORDER BY 2 DESC;",
                conn)

            pop_air = pop_air.set_index(['DEPARTURE_AIRPORT'])
            st.line_chart(pop_air)

        with right_column:
            st_lottie(lottie_airport, height=300, key="airport")

with tab4:
    # st.header("Popular Routes")
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("Popular Routes")
            # Query for average fuel burn across airlines
            pop_routes = pd.read_sql(
                f"WITH popular_routes AS (SELECT DEPARTURE_AIRPORT,ARRIVAL_AIRPORT,COUNT(*) AS nb_flights FROM SCHEDULED_FLIGHT_EMISSIONS GROUP BY 1,2 ),ranked_routes AS (SELECT DEPARTURE_AIRPORT,ARRIVAL_AIRPORT,ROW_NUMBER() OVER(PARTITION BY DEPARTURE_AIRPORT ORDER BY nb_flights DESC) AS rank FROM popular_routes) SELECT DEPARTURE_AIRPORT as origin, ARRIVAL_AIRPORT as destination FROM ranked_routes WHERE rank <= 3 ORDER BY rank LIMIT 10;",
                conn)
            # pop_air = pop_air.set_index(['DEPARTURE_AIRPORT'])
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

            pop_routes = pop_routes.replace({"origin": pop_routes_origin_dict, "destination": pop_routes_dest_dict})
            st.dataframe(pop_routes)

        with right_column:
            st_lottie(lottie_emission, height=300, key="coding")

        st.write(
            "[Airport Codes>](https://www.world-airport-codes.com/alphabetical/airport-code/a.html?page=1)")
# ---- CONTACT ----
# with st.container():
#     st.write("---")
#     st.header("Get In Touch With Us!")
#     st.write("##")
#
#     # Contact Us section
#     contact_form = """
#     <form action="https://formsubmit.co/adrane.aws@gmail.com" method="POST">
#         <input type="hidden" name="_captcha" value="false">
#         <input type="text" name="name" placeholder="Your name" required>
#         <input type="email" name="email" placeholder="Your email" required>
#         <textarea name="message" placeholder="Your message here" required></textarea>
#         <button type="submit">Send</button>
#     </form>
#     """
#     left_column, right_column = st.columns(2)
#     with left_column:
#         st.markdown(contact_form, unsafe_allow_html=True)
#     with right_column:
#         st.empty()
