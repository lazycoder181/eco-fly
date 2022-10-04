import requests
import pandas as pd
from pandas import json_normalize

apiKey = "MMTSfNNfFEgdoHZrfy73sBJpfJZF1nym"
apiUrl = "https://aeroapi.flightaware.com/aeroapi/"

payload = {'max_pages': 15}
auth_header = {'x-apikey': apiKey}
startDate = "2022-09-30"
endDate = "2022-09-30"

origin = "MEL"
#     # , "SYD", "BNE", "PER", "ADL", "OOL", "CNS", "CBR", "HBA", "DRW", "TSW", "LST", "NTL", "MCY", "MKY",
#     #       "AVV", "ASP", "ROK", "BNK", "AYQ", "KTA", "HTI", "PPP", "BME", "CFS", "PHE", "ZNE", "KGI", "ABX", "GLT",
#     #       "MQL", "PQQ", "ISA", "DBO"]  # Australian airports

res = requests.get(apiUrl + f"schedules/{startDate}/{endDate}?origin={origin}",
                   params=payload, headers=auth_header)

if res.status_code == 200:
    dictr = res.json()
    recs = dictr['scheduled']
    # Normalise for dataframe
    df_flight = json_normalize(recs)
    print(df_flight)
    # Export
    df_flight.to_csv("flightware_data.csv")

else:
    print("Error executing request")
