import pandas as pd
import json


def retrieve_data(bucket_name: str, object_key: str, s3_client):

    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        data = json.loads(response["Body"].read().decode('utf-8'))
        df = pd.DataFrame(data)
        return df

    except s3_client.exceptions.NoSuchKey:
        raise KeyError(f"The key '{object_key}' does not exist.")


def transform_sales_order(sales_order_df):
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
    dim_staff = staff_df.copy()
    dim_staff = dim_staff.merge(department_df[['department_id', 'department_name', 'location']],
                                on='department_id', how='left')
    return dim_staff[["staff_id", "first_name", "last_name", "department_name",
                      "location", "email_address"]]


def transform_location(address_df):
    dim_location = address_df.copy()
    dim_location = dim_location.rename(columns={
        'address_id': 'location_id'
        })
    return dim_location[["location_id", "address_line_1", "address_line_2", "district", "city",
                        "postal_code", "country", "phone"]]


def transform_currency(currency_df):
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
    dim_design = design_df.copy()
    return dim_design[[
        'design_id', 'design_name', 'file_location', 'file_name'
    ]]


def transform_counterparty(counterparty_df, address_df):
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


def transform_to_star_schema(sales_order_df, staff_df, address_df, currency_df,
                             design_df, counterparty_df, department_df):
    fact_sales_order = transform_sales_order(sales_order_df)
    dim_date = create_dim_date('2024-01-01', '2030-01-01')
    dim_staff = transform_staff(staff_df, department_df)
    dim_location = transform_location(address_df)
    dim_currency = transform_currency(currency_df)
    dim_design = transform_design(design_df)
    dim_counterparty = transform_counterparty(counterparty_df, address_df)
    return fact_sales_order, dim_date, dim_staff, dim_location, \
        dim_currency, dim_design, dim_counterparty


def write_packet_id(packet_id: int, table_name: str, ssm_client) -> None:
    """

    Write table_name : packet_id key value pair to Parameter Store

    Args:
        table_name (string)
        packet_id(int)

    Raises:
        KeyError: table_name does not exist
        ConnectionError : connection issue to parameter store

    Returns:
        None
    """
    try:
        print("writing ")
        ssm_client.put_parameter(
            Name=f"/processing/{table_name}/latest_packet_id",
            Type="String",
            Description=(
                "Latest packet_id of data processed "
                f"from Totesys database for {table_name} table"
            ),
            Value=str(packet_id),
            Overwrite=True,
        )
    except Exception as e:
        print(f"The packet ID could not be written: {e}")


def get_packet_id(table_name: str, ssm_client) -> int:
    """
    From parameter store retrieves table_name : packet_id key value pair

    Args:
        table_name (string)


    Raises:
        KeyError: table_name does not exist
        ConnectionError : connection issue to parameter store

    Returns:
        packet_id(int)

    """
    try:
        response = ssm_client.get_parameter(Name=("/processing/"+table_name+"/latest_packet_id"))
        id = response["Parameter"]["Value"]
        return int(id)

    except ssm_client.exceptions.ParameterNotFound:
        raise KeyError(f"Table name '{table_name}' does not have any recorded packets.")


# def write_table_data_to_s3(
#     dict_name dict,
#     bucket_name: str,
#     packet_id: int,
#     s3_client,
# ) -> None:
# """
# Write file to S3 bucket in Parquet format

# Args:
#     table_name (string)
#     table_data (list) : list of dictionaries all data in table,
#         one dictionary per row keys will be column headings
#     bucket_name (string)
#     packet_id (string)
#     s3_client (boto3 s3 client)

# Raises:
#     FileExistsError: S3 object already exists with the same name
#     ConnectionError : connection issue to S3 bucket

# Returns:
#     None
# """
