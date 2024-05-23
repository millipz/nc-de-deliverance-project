import pandas as pd
import json
import io
import boto3
from datetime import datetime, date

s3_client = boto3.client('s3')


def retrieve_data(bucket_name: str, object_key: str, s3_client):
    """
    Load data from an s3 object (json lines) into a pandas dataframe

    Args:
        bucket_name (str): bucket where the object is stored
        object_key (str): key of data object
        client (boto3 s3 Client)

    Raises:
        KeyError: table_name does not exist
        ConnectionError : connection issue to parameter store

    Returns:
        data: pandas dataframe
    """
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        data = json.loads(response["Body"].read().decode('utf-8'))
        df = pd.DataFrame(data)
        return df

    except s3_client.exceptions.NoSuchKey:
        raise KeyError(f"The key '{object_key}' does not exist.")


def transform_sales_order(sales_order_df):
    """
    Transform loaded sales order data into star schema
        - splits out time and date data into seperate columns
        - renames staff_id to sales_staff_id
        - removes unwanted columns

    Args:
        sales_order_df (pandas dataframe): original data

    Returns:
        data (pandas dataframe): transformed data
    """
    fact_sales_order = sales_order_df.copy()

    fact_sales_order['created_date'] = pd.to_datetime(fact_sales_order['created_at']).dt.date
    fact_sales_order['created_time'] = pd.to_datetime(fact_sales_order['created_at']).dt.time
    fact_sales_order['last_updated_date'] = \
        pd.to_datetime(fact_sales_order['last_updated']).dt.date
    fact_sales_order['last_updated_time'] = \
        pd.to_datetime(fact_sales_order['last_updated']).dt.time

    fact_sales_order.rename(columns={
        'staff_id': 'sales_staff_id',
    }, inplace=True)

    return fact_sales_order[[
        'sales_order_id',
        'created_date',
        'created_time',
        'last_updated_date',
        'last_updated_time',
        'sales_staff_id',
        'counterparty_id',
        'units_sold',
        'unit_price',
        'currency_id',
        'design_id',
        'agreed_payment_date',
        'agreed_delivery_date',
        'agreed_delivery_location_id']]


def create_dim_date(start_date, end_date):
    """
    Creates a table of dates in the given range
    with columns for:
        - year
        - month
        - month name
        - day of month
        - day of year
        - day of week
        - quarter


    Args:
        start_date (datetime)
        end_date (datetime)

    Returns:
        dates (pandas dataframe)
    """
    date_range = pd.date_range(start=start_date, end=end_date)
    dim_date = pd.DataFrame(date_range, columns=['date_id'])
    dim_date['year'] = dim_date['date_id'].dt.year
    dim_date['month'] = dim_date['date_id'].dt.month
    dim_date['day'] = dim_date['date_id'].dt.day
    dim_date['day_of_week'] = dim_date['date_id'].dt.weekday
    dim_date['day_name'] = dim_date['date_id'].dt.day_name()
    dim_date['month_name'] = dim_date['date_id'].dt.month_name()
    dim_date['quarter'] = dim_date['date_id'].dt.quarter
    return dim_date


def transform_staff(staff_df, department_df):
    """
    Transform loaded staff order data into star schema
        - adds a location by reference to department table

    Args:
        staff_df (pandas dataframe): original data
        department_df (pandas dataframe): department data for location

    Returns:
        data (pandas dataframe): transformed data
    """
    dim_staff = staff_df.copy()
    dim_staff = dim_staff.merge(department_df[['department_id', 'department_name', 'location']],
                                on='department_id', how='left')
    return dim_staff[["staff_id", "first_name", "last_name", "department_name",
                      "location", "email_address"]]


def transform_location(address_df):
    """
    Transform loaded address order data into star schema
        - renames address_id to location_id

    Args:
        address_df (pandas dataframe): original data

    Returns:
        data (pandas dataframe): transformed data
    """
    dim_location = address_df.copy()
    dim_location = dim_location.rename(columns={
        'address_id': 'location_id'
        })
    return dim_location[["location_id", "address_line_1", "address_line_2", "district", "city",
                        "postal_code", "country", "phone"]]


def transform_currency(currency_df):
    """
    Transform loaded currency data into star schema
        - adds currency names from currency codes
        - remove unwanted last_updated column

    Args:
        currency_df (pandas dataframe): original data

    Returns:
        data (pandas dataframe): transformed data
    """
    def get_currency_name(currency_code):
        currency_name_map = {
            'AED': 'United Arab Emirates Dirham',
            'AFN': 'Afghan Afghani',
            'ALL': 'Albanian Lek',
            'AMD': 'Armenian Dram',
            'ANG': 'Netherlands Antillean Guilder',
            'AOA': 'Angolan Kwanza',
            'ARS': 'Argentine Peso',
            'AUD': 'Australian Dollar',
            'AWG': 'Aruban Florin',
            'AZN': 'Azerbaijani Manat',
            'BAM': 'Bosnia-Herzegovina Convertible Mark',
            'BBD': 'Barbadian Dollar',
            'BDT': 'Bangladeshi Taka',
            'BGN': 'Bulgarian Lev',
            'BHD': 'Bahraini Dinar',
            'BIF': 'Burundian Franc',
            'BMD': 'Bermudian Dollar',
            'BND': 'Brunei Dollar',
            'BOB': 'Bolivian Boliviano',
            'BRL': 'Brazilian Real',
            'BSD': 'Bahamian Dollar',
            'BTN': 'Bhutanese Ngultrum',
            'BWP': 'Botswana Pula',
            'BYN': 'Belarusian Ruble',
            'BZD': 'Belize Dollar',
            'CAD': 'Canadian Dollar',
            'CDF': 'Congolese Franc',
            'CHF': 'Swiss Franc',
            'CLP': 'Chilean Peso',
            'CNY': 'Chinese Yuan',
            'COP': 'Colombian Peso',
            'CRC': 'Costa Rican Colón',
            'CUP': 'Cuban Peso',
            'CVE': 'Cape Verdean Escudo',
            'CZK': 'Czech Koruna',
            'DJF': 'Djiboutian Franc',
            'DKK': 'Danish Krone',
            'DOP': 'Dominican Peso',
            'DZD': 'Algerian Dinar',
            'EGP': 'Egyptian Pound',
            'ERN': 'Eritrean Nakfa',
            'ETB': 'Ethiopian Birr',
            'EUR': 'Euro',
            'FJD': 'Fijian Dollar',
            'FKP': 'Falkland Islands Pound',
            'FOK': 'Faroese Króna',
            'GBP': 'British Pound',
            'GEL': 'Georgian Lari',
            'GGP': 'Guernsey Pound',
            'GHS': 'Ghanaian Cedi',
            'GIP': 'Gibraltar Pound',
            'GMD': 'Gambian Dalasi',
            'GNF': 'Guinean Franc',
            'GTQ': 'Guatemalan Quetzal',
            'GYD': 'Guyanese Dollar',
            'HKD': 'Hong Kong Dollar',
            'HNL': 'Honduran Lempira',
            'HRK': 'Croatian Kuna',
            'HTG': 'Haitian Gourde',
            'HUF': 'Hungarian Forint',
            'IDR': 'Indonesian Rupiah',
            'ILS': 'Israeli New Shekel',
            'IMP': 'Isle of Man Pound',
            'INR': 'Indian Rupee',
            'IQD': 'Iraqi Dinar',
            'IRR': 'Iranian Rial',
            'ISK': 'Icelandic Króna',
            'JEP': 'Jersey Pound',
            'JMD': 'Jamaican Dollar',
            'JOD': 'Jordanian Dinar',
            'JPY': 'Japanese Yen',
            'KES': 'Kenyan Shilling',
            'KGS': 'Kyrgyzstani Som',
            'KHR': 'Cambodian Riel',
            'KID': 'Kiribati Dollar',
            'KMF': 'Comorian Franc',
            'KRW': 'South Korean Won',
            'KWD': 'Kuwaiti Dinar',
            'KYD': 'Cayman Islands Dollar',
            'KZT': 'Kazakhstani Tenge',
            'LAK': 'Lao Kip',
            'LBP': 'Lebanese Pound',
            'LKR': 'Sri Lankan Rupee',
            'LRD': 'Liberian Dollar',
            'LSL': 'Lesotho Loti',
            'LYD': 'Libyan Dinar',
            'MAD': 'Moroccan Dirham',
            'MDL': 'Moldovan Leu',
            'MGA': 'Malagasy Ariary',
            'MKD': 'Macedonian Denar',
            'MMK': 'Myanmar Kyat',
            'MNT': 'Mongolian Tögrög',
            'MOP': 'Macanese Pataca',
            'MRU': 'Mauritanian Ouguiya',
            'MUR': 'Mauritian Rupee',
            'MVR': 'Maldivian Rufiyaa',
            'MWK': 'Malawian Kwacha',
            'MXN': 'Mexican Peso',
            'MYR': 'Malaysian Ringgit',
            'MZN': 'Mozambican Metical',
            'NAD': 'Namibian Dollar',
            'NGN': 'Nigerian Naira',
            'NIO': 'Nicaraguan Córdoba',
            'NOK': 'Norwegian Krone',
            'NPR': 'Nepalese Rupee',
            'NZD': 'New Zealand Dollar',
            'OMR': 'Omani Rial',
            'PAB': 'Panamanian Balboa',
            'PEN': 'Peruvian Sol',
            'PGK': 'Papua New Guinean Kina',
            'PHP': 'Philippine Peso',
            'PKR': 'Pakistani Rupee',
            'PLN': 'Polish Złoty',
            'PYG': 'Paraguayan Guaraní',
            'QAR': 'Qatari Riyal',
            'RON': 'Romanian Leu',
            'RSD': 'Serbian Dinar',
            'RUB': 'Russian Ruble',
            'RWF': 'Rwandan Franc',
            'SAR': 'Saudi Riyal',
            'SBD': 'Solomon Islands Dollar',
            'SCR': 'Seychellois Rupee',
            'SDG': 'Sudanese Pound',
            'SEK': 'Swedish Krona',
            'SGD': 'Singapore Dollar',
            'SHP': 'Saint Helena Pound',
            'SLL': 'Sierra Leonean Leone',
            'SOS': 'Somali Shilling',
            'SRD': 'Surinamese Dollar',
            'SSP': 'South Sudanese Pound',
            'STN': 'São Tomé and Príncipe Dobra',
            'SYP': 'Syrian Pound',
            'SZL': 'Eswatini Lilangeni',
            'THB': 'Thai Baht',
            'TJS': 'Tajikistani Somoni',
            'TMT': 'Turkmenistani Manat',
            'TND': 'Tunisian Dinar',
            'TOP': 'Tongan Paʻanga',
            'TRY': 'Turkish Lira',
            'TTD': 'Trinidad and Tobago Dollar',
            'TVD': 'Tuvaluan Dollar',
            'TWD': 'New Taiwan Dollar',
            'TZS': 'Tanzanian Shilling',
            'UAH': 'Ukrainian Hryvnia',
            'UGX': 'Ugandan Shilling',
            'USD': 'US Dollar',
            'UYU': 'Uruguayan Peso',
            'UZS': 'Uzbekistani Soʻm',
            'VES': 'Venezuelan Bolívar',
            'VND': 'Vietnamese Đồng',
            'VUV': 'Vanuatu Vatu',
            'WST': 'Samoan Tālā',
            'XAF': 'Central African CFA Franc',
            'XCD': 'East Caribbean Dollar',
            'XDR': 'Special Drawing Rights',
            'XOF': 'West African CFA Franc',
            'XPF': 'CFP Franc',
            'YER': 'Yemeni Rial',
            'ZAR': 'South African Rand',
            'ZMW': 'Zambian Kwacha',
            'ZWL': 'Zimbabwean Dollar'
        }
        return currency_name_map.get(currency_code, 'Unknown')
    dim_currency = currency_df.copy()
    dim_currency['currency_name'] = dim_currency['currency_code'].apply(get_currency_name)
    return dim_currency[["currency_id", "currency_code", "currency_name"]]


def transform_design(design_df):
    """
    Transform loaded design data into star schema
        - remove unwanted columns

    Args:
        design_df (pandas dataframe): original data

    Returns:
        data (pandas dataframe): transformed data
    """
    dim_design = design_df.copy()
    return dim_design[[
        'design_id', 'design_name', 'file_location', 'file_name'
    ]]


def transform_counterparty(counterparty_df, address_df):
    """
    Transform loaded counterparty data into star schema
        - lookup address in address data and add to table
        - renames columns to suit star schema
        - removes unwanted columns

    Args:
        counterparty_df (pandas dataframe): original data
        address_df (pandas dataframe): address data for reference

    Returns:
        data (pandas dataframe): transformed data
    """
    dim_counterparty = counterparty_df.copy()
    dim_counterparty = dim_counterparty.merge(address_df, left_on='legal_address_id',
                                              right_on='address_id', how='left')
    dim_counterparty = dim_counterparty.rename(columns={
        'address_line_1': 'counterparty_legal_address_line_1',
        'address_line_2': 'counterparty_legal_address_line_2',
        'district': 'counterparty_legal_district',
        'city': 'counterparty_legal_city',
        'postal_code': 'counterparty_legal_postal_code',
        'country': 'counterparty_legal_country',
        'phone': 'counterparty_legal_phone_number'
    })
    return dim_counterparty[['counterparty_id', 'counterparty_legal_name',
                             'counterparty_legal_address_line_1',
                             'counterparty_legal_address_line_2',
                             'counterparty_legal_district', 'counterparty_legal_city',
                             'counterparty_legal_postal_code', 'counterparty_legal_country',
                             'counterparty_legal_phone_number']]


def write_data_to_s3(df: pd.DataFrame,
                     table_name: str,
                     bucket_name: str,
                     packet_id: int,
                     s3_client):
    """
    Write dataframe to S3 bucket in Parquet format

    Args:
        df (pd.DataFrame): DataFrame to write
        table_name (string)
        bucket_name (string)
        packet_id (string)
        s3_client (boto3 s3 client)

    Raises:
        FileExistsError: S3 object already exists with the same name
        ConnectionError : connection issue to S3 bucket

    Returns:
        None
    """
    buffer = io.BytesIO()
    df.to_parquet(buffer, engine='fastparquet')
    time_format = "%H%M%S%f"
    key = (
        f"{date.today()}/{table_name}_"
        f"{str(packet_id).zfill(8)}_"
        f"processed_"
        f"{datetime.now().strftime(time_format)}.parquet"
    )
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=buffer.getvalue())


def get_timestamp(table_name: str, ssm_client) -> datetime:
    """
    Return timestamp showing most recent entry from the given table
    that has been processed by the ingestion lambda.

    Args:
        table_name (str): table name to get timestamp for
        client (boto3 SSM Client)

    Raises:
        KeyError: table_name does not exist
        ConnectionError : connection issue to parameter store

    Returns:
        timestamp (datetime timestamp) : stored timestamp of most recent
        ingested data for given table
    """
    try:
        response = ssm_client.get_parameter(
            Name=(table_name + "_latest_extracted_timestamp")
        )

        timestamp = response["Parameter"]["Value"]
        return datetime.fromisoformat(timestamp)

    except ssm_client.exceptions.ParameterNotFound:
        raise KeyError(
            f"Table name '{table_name}' does not have any recorded latest data."
        )

    # TODO connection errors should be checked when connecting with
    # credentials so this might not be needed here
    # except (ssm_client.exceptions.ConnectionError):
    #     raise ConnectionError("Connection issue to Parameter Store.")


def write_timestamp(timestamp: datetime, table_name: str, ssm_client) -> None:
    """

    Writes timestamp to parameter store for given table

    Args:
        timestamp (timestamp) : timestamp of latest extracted data
        table_name (str) : table name to store timestamp for
        client (boto3 SSM Client) : client passed in to avoid recreating for each invocation

    Raises:
        ConnectionError : connection issue to parameter store

    Returns:
        None
    """
    try:
        ssm_client.put_parameter(
            Name=f"{table_name}_latest_extracted_timestamp",
            Type="String",
            Description=(
                "Latest timestamp of data ingested"
                f"from Totesys database for {table_name} table"
            ),
            Value=timestamp.isoformat(timespec="milliseconds"),
            Overwrite=True,
        )
    except Exception as e:
        print(f"The timestamp could not be written: {e}")
