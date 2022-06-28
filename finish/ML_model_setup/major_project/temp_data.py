import pandas as pd

# PS              MERRA-2 Surface Pressure (kPa)
# T2M             MERRA-2 Temperature at 2 Meters (C)
# QV2M            MERRA-2 Specific Humidity at 2 Meters (g/kg)
# PRECTOTCORR     MERRA-2 Precipitation Corrected (mm/day)

def myfun(tf):
    arr = [[] for i in range(16)]

    for i in tf[tf.columns].values:
        if i[1] <= 2015:
            arr[i[1] - 2000].append(i[-1])
    # print(len(arr))
    # print(arr[-1])
    return arr
tf = pd.read_csv("temperature.csv")

print(tf.head())



