import os, time
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL



load_dotenv("../config/.env")
DATABASE_PASS = os.environ.get("DATABASE_PASS")




# ---------------- Set up engine  ---------------------
url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password=os.getenv("DATABASE_PASS"),  # No need to special change symbols now
    host="localhost",
    port=3306,
    database="iplraw",
)
engine = create_engine(url)



# ------------  Check time to Load first table  ---------------
starttime = time.perf_counter()


# Read in chunks so large files don't blow up memory
first_chunk = True
for chunk in pd.read_csv("../data/archive/matches.csv", chunksize=50_000):

    # Load raw data into sql db
    chunk.to_sql(
        "matches_raw",              # First table name
        con=engine,
        if_exists="replace" if first_chunk else "append",       # creates table first time then append
        index=False,
        method="multi",
        chunksize=5_000,
    )
    first_chunk = False

endtime = time.perf_counter()
print(f"Loaded First table in {endtime-starttime} seconds")
# ---------------------------------------------------------------




# ------------  Check time to Load second table  ---------------
starttime = time.perf_counter()

second_chunk = True
for chunk in pd.read_csv("../data/archive/deliveries.csv", chunksize=50_000):

    chunk.to_sql(
        "deliveries_raw",                  # Second table name
        con=engine,
        if_exists="replace" if second_chunk else "append",       # creates table first time then append
        index=False,
        method="multi",
        chunksize=5_000,
    )
    second_chunk = False

endtime = time.perf_counter()
print(f"Loaded Second table in {endtime-starttime} seconds")

# ------------------------------------------------------------