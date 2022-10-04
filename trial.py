import pandas as pd
import snowflake.connector
import streamlit as st
from matplotlib import pyplot
# Define connection parameters

conn = snowflake.connector.connect(user='jedi1', password='Jedi1234!', account='ur88629.ap-southeast-2',
                                   warehouse='Emission',
                                   database='MARKETPLACE_EMISSIONS', schema='PROOF_OF_CONCEPT')
op_airlines = pd.read_sql(
    "SELECT DISTINCT OPERATING_AIRLINE FROM MARKETPLACE_EMISSIONS.PROOF_OF_CONCEPT.SCHEDULED_FLIGHT_EMISSIONS;",
    conn)

# Providing options to users for exploring the OPERATING flights
option = st.selectbox('SELECT OPERATING AIRLINE:', op_airlines)

# Query for average fuel burn across airlines
avg_burn = pd.read_sql(f"SELECT DISTINCT AIRLINECODE, AVG(ESTIMATED_FUEL_BURN_TONNES) FROM SCHEDULED_FLIGHT_EMISSIONS GROUP BY AIRLINECODE,ESTIMATED_FUEL_BURN_TONNES;", conn, params={"option": option})

avg_burn = avg_burn.set_index(['AIRLINECODE'])

# Query for average CO2 emission
avg_emission = pd.read_sql(f"SELECT DISTINCT AIRLINECODE, AVG(ESTIMATED_CO2_EMISSIONS_TONNES) FROM SCHEDULED_FLIGHT_EMISSIONS GROUP BY AIRLINECODE,ESTIMATED_CO2_EMISSIONS_TONNES;", conn, params={"option": option})

avg_emission = avg_emission.set_index(['AIRLINECODE'])
# Line chart to visualise
# = %(option)
# f"Average Fuel consumption in {option} is "
f"Average Fuel consumption based on airlinecode is "
st.bar_chart(avg_burn)

f"Average CO2 emission based on airlinecode is "
st._arrow_line_chart(avg_emission)

# SELECT SCHEDULED_FLIGHT_EMISSIONS.AIRLINECODE, SUM(SCHEDULED_FLIGHT_EMISSIONS.ESTIMATED_FUEL_BURN_TONNES) FROM MARKETPLACE_EMISSIONS.PROOF_OF_CONCEPT.SCHEDULED_FLIGHT_EMISSIONS GROUP BY SCHEDULED_FLIGHT_EMISSIONS.AIRLINECODE,SCHEDULED_FLIGHT_EMISSIONS.ESTIMATED_FUEL_BURN_TONNES