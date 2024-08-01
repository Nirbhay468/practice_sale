import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, inspect

# app = FastAPI()

# Database configuration
DATABASE_URI = 'postgresql+psycopg2://myuser:mypassword@localhost:5432/mydatabase'

# CSV file paths

BRAND_DATA_CSV = "/Users/nirbhaysingh.vc/Desktop/Dummy_data/brand_data.csv"
PRODUCT_DETAILS_CSV = "/Users/nirbhaysingh.vc/Desktop/Dummy_data/product_details.csv"
SALES_DATA_CSV = "/Users/nirbhaysingh.vc/Desktop/Dummy_data/sales_data.csv"
CATEGORY_SHARE_DATA_CSV = "/Users/nirbhaysingh.vc/Desktop/Dummy_data/category_share_data.csv"
PRODUCT_CATEGORY_MAPPING_CSV = "/Users/nirbhaysingh.vc/Desktop/Dummy_data/product_category_mapping.csv"
CATEGORY_DETAILS_CSV = "/Users/nirbhaysingh.vc/Desktop/Dummy_data/category_details.csv"

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URI)

def load_csv_to_db():
    try:
        print("Start of load_csv_to_db")
        engine = create_engine(DATABASE_URI)

        # Load CSV files into DataFrames
        sales_data = pd.read_csv(SALES_DATA_CSV)
        category_share_data = pd.read_csv(CATEGORY_SHARE_DATA_CSV)
        brand_data_csv = pd.read_csv(BRAND_DATA_CSV)
        product_details_csv = pd.read_csv(PRODUCT_DETAILS_CSV)
        product_category_mapping = pd.read_csv(PRODUCT_CATEGORY_MAPPING_CSV)
        category_details_csv = pd.read_csv(CATEGORY_DETAILS_CSV)

        # Iterate over each DataFrame and insert rows sequentially
        for df, table_name in [
            (brand_data_csv, 'brand_data'),
            (product_details_csv, 'product_details'),
            (sales_data, 'sales_data'),
            (category_details_csv, 'category_details'),
            (category_share_data, 'category_share_data'),
            (product_category_mapping, 'product_category_mapping'),
        ]:
            df.to_sql(table_name, engine, if_exists='append', index=False)
            print(f"Inserted data into {table_name} successfully!")

        print("Data loaded successfully!")

    except SQLAlchemyError as e:
        print(f"Error: {e}")
