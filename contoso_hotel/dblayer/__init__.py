import os, re
from typing import Dict, List, Union, Iterable, Tuple
from enum import Enum
from datetime import datetime

class SQLMode(Enum):
    INSERT = 1
    UPDATE = 2



def get_connection_string(name : str) -> str:
    name = str(name).strip().upper()
    if name != "MSSQL_CONNECTION_STRING" and name != "POSTGRES_CONNECTION_STRING":
        raise ValueError("Invalid database name (only 'MSSQL_CONNECTION_STRING' and 'POSTGRES_CONNECTION_STRING' are supported)")
    connectionString = ""
    secretStoreFile = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'secrets-store', name)
    if os.path.isfile(secretStoreFile):
        #print("Reading connection string from secrets store")
        with open(secretStoreFile, 'r') as file:
            connectionString = file.read().strip()
    else:
        #print("Reading connection string from environment variable")
        connectionString = os.getenv(name, '')
    if not connectionString:
        raise ValueError("Connection string is empty")
    return connectionString

def get_defined_database() -> Tuple[str, str]:
    try:
        return get_connection_string("MSSQL_CONNECTION_STRING"), "MSSQL_CONNECTION_STRING"
    except:
        pass
    try:
        return get_connection_string("POSTGRES_CONNECTION_STRING"), "POSTGRES_CONNECTION_STRING"
    except:
        pass
    raise ValueError("Connection string is empty, either use MSSQL_CONNECTION_STRING or POSTGRES_CONNECTION_STRING")

def parse_connection_string_to_dict(s : str, allowedArgs : Union[List[str], Dict[List,List]]) -> Dict[str, Union[int, str, float, bool]]:
    args = {}
    if isinstance(allowedArgs, list):
        # convert list to dictionary
        allowedArgs = {str(arg).lower(): "" for arg in allowedArgs}
    elif isinstance(allowedArgs, dict):
        # ensure all values are converted to strings
        allowedArgs = {str(arg).lower(): str(allowedArgs[arg]) for arg in allowedArgs}
    else:
        raise ValueError("allowedArgs must be a list or a dictionary")
    for part in split_string_with_escaping(s):
        parts = part.split("=")
        if len(parts) != 2:
            continue
        parts[0] = parts[0].strip().lower()
        if parts[0] not in allowedArgs.keys():
            print("    is not in allowed args " + parts[0])
            continue
        if allowedArgs[parts[0]] == "":
            args[parts[0]] = parts[1]
        else:
            if re.match(allowedArgs[parts[0]], parts[1]):
                args[parts[0]] = parts[1]
    return args

def split_string_with_escaping(s):
    pattern = r'(?<!\\);'
    result = re.split(pattern, s)
    result = [part.replace(r'\;', ';').replace(r'\\;', r'\;') for part in result]
    return result


dbconnectionstring, dbconnectionstringname = get_defined_database()


if dbconnectionstringname == "MSSQL_CONNECTION_STRING":
    from . import mssqldblayer

    def longsqlrequest() -> int:
        return mssqldblayer.longsqlrequest()

    def create_booking(hotelId : int, visitorId : int, checkin : datetime, checkout : datetime, adults : int, kids : int, babies : int, rooms : int = None, price : float = None, bookingId : int = None) -> Dict[str, Union[int, str, float, bool]]:
        return mssqldblayer.create_booking(hotelId, visitorId, checkin, checkout, adults, kids, babies, rooms, price, bookingId)

    def delete_booking(bookingId : int) -> bool:
        return mssqldblayer.delete_booking(bookingId)

    def get_booking(bookingId : int) -> Dict[str, Union[int, str, float, bool]]:
        return mssqldblayer.get_booking(bookingId)

    def get_bookings(visitorId : int = None, hotelId : int = None, fromdate : datetime = None, untildate : datetime = None) -> Iterable[Dict[str, Union[int, str, float, bool]]]:
        return mssqldblayer.get_bookings(visitorId, hotelId, fromdate, untildate)

    def create_visitor(firstname : str, lastname : str, visitorId : int = None) -> Dict[str, Union[int, str, float, bool]]:
        return mssqldblayer.create_visitor(firstname, lastname, visitorId)

    def update_visitor(firstname : str, lastname : str, visitorId : int) -> Dict[str, Union[int, str, float, bool]]:
        return mssqldblayer.update_visitor(firstname, lastname, visitorId)

    def manage_visitor(firstname : str, lastname : str, visitorId : int = None, sqlmode : SQLMode = 1) -> Dict[str, Union[int, str, float, bool]]:
        return mssqldblayer.manage_visitor(firstname, lastname, visitorId, sqlmode)

    def delete_visitor(visitorId : int) -> bool:
        return mssqldblayer.delete_visitor(visitorId)

    def get_visitor(visitorId : int) -> Dict[str, Union[int, str, float, bool]]:
        return mssqldblayer.get_visitor(visitorId)

    def get_visitors(name : str = "", exactMatch : bool = False) -> Iterable[Dict[str, Union[int, str, float, bool]]]:
        return mssqldblayer.get_visitors(name, exactMatch)

    def create_hotel(hotelname : str, pricePerNight : float, hotelId : int = None) -> Dict[str, Union[int, str, float, bool]]:
        return mssqldblayer.create_hotel(hotelname, pricePerNight, hotelId)

    def update_hotel(hotelname : str, pricePerNight : float, hotelId : int) -> Dict[str, Union[int, str, float, bool]]:
        return mssqldblayer.update_hotel(hotelname, pricePerNight, hotelId)

    def manage_hotel(hotelname : str, pricePerNight : float, hotelId : int = None, sqlmode : SQLMode = 1) -> Dict[str, Union[int, str, float, bool]]:
        return mssqldblayer.manage_hotel(hotelname, pricePerNight, hotelId, sqlmode)
    def delete_hotel(hotelId : int) -> bool:
        return mssqldblayer.delete_hotel(hotelId)

    def get_hotel(hotelId : int) -> Dict[str, Union[int, str, float, bool]]:
        return mssqldblayer.get_hotel(hotelId)

    def get_hotels(name : str = "", exactMatch : bool = False) -> Iterable[Dict[str, Union[int, str, float, bool]]]:
        return mssqldblayer.get_hotels(name, exactMatch)

    def allTablesExists() -> bool:
        return mssqldblayer.allTablesExists()

    def setupDb(drop_schema : bool, create_schema : bool, populate_data : bool):
        return mssqldblayer.setupDb(drop_schema, create_schema, populate_data)

elif dbconnectionstringname == "POSTGRES_CONNECTION_STRING":
    from . import postgresdblayer

    def longsqlrequest() -> int:
        return postgresdblayer.longsqlrequest()

    def create_booking(hotelId : int, visitorId : int, checkin : datetime, checkout : datetime, adults : int, kids : int, babies : int, rooms : int = None, price : float = None, bookingId : int = None) -> Dict[str, Union[int, str, float, bool]]:
        return postgresdblayer.create_booking(hotelId, visitorId, checkin, checkout, adults, kids, babies, rooms, price, bookingId)

    def delete_booking(bookingId : int) -> bool:
        return postgresdblayer.delete_booking(bookingId)

    def get_booking(bookingId : int) -> Dict[str, Union[int, str, float, bool]]:
        return postgresdblayer.get_booking(bookingId)

    def get_bookings(visitorId : int = None, hotelId : int = None, fromdate : datetime = None, untildate : datetime = None) -> Iterable[Dict[str, Union[int, str, float, bool]]]:
        return postgresdblayer.get_bookings(visitorId, hotelId, fromdate, untildate)

    def create_visitor(firstname : str, lastname : str, visitorId : int = None) -> Dict[str, Union[int, str, float, bool]]:
        return postgresdblayer.create_visitor(firstname, lastname, visitorId)

    def update_visitor(firstname : str, lastname : str, visitorId : int) -> Dict[str, Union[int, str, float, bool]]:
        return postgresdblayer.update_visitor(firstname, lastname, visitorId)

    def manage_visitor(firstname : str, lastname : str, visitorId : int = None, sqlmode : SQLMode = 1) -> Dict[str, Union[int, str, float, bool]]:
        return postgresdblayer.manage_visitor(firstname, lastname, visitorId, sqlmode)

    def delete_visitor(visitorId : int) -> bool:
        return postgresdblayer.delete_visitor(visitorId)

    def get_visitor(visitorId : int) -> Dict[str, Union[int, str, float, bool]]:
        return postgresdblayer.get_visitor(visitorId)

    def get_visitors(name : str = "", exactMatch : bool = False) -> Iterable[Dict[str, Union[int, str, float, bool]]]:
        return postgresdblayer.get_visitors(name, exactMatch)

    def create_hotel(hotelname : str, pricePerNight : float, hotelId : int = None) -> Dict[str, Union[int, str, float, bool]]:
        return postgresdblayer.create_hotel(hotelname, pricePerNight, hotelId)

    def update_hotel(hotelname : str, pricePerNight : float, hotelId : int) -> Dict[str, Union[int, str, float, bool]]:
        return postgresdblayer.update_hotel(hotelname, pricePerNight, hotelId)

    def manage_hotel(hotelname : str, pricePerNight : float, hotelId : int = None, sqlmode : SQLMode = 1) -> Dict[str, Union[int, str, float, bool]]:
        return postgresdblayer.manage_hotel(hotelname, pricePerNight, hotelId, sqlmode)
    def delete_hotel(hotelId : int) -> bool:
        return postgresdblayer.delete_hotel(hotelId)

    def get_hotel(hotelId : int) -> Dict[str, Union[int, str, float, bool]]:
        return postgresdblayer.get_hotel(hotelId)

    def get_hotels(name : str = "", exactMatch : bool = False) -> Iterable[Dict[str, Union[int, str, float, bool]]]:
        return postgresdblayer.get_hotels(name, exactMatch)

    def allTablesExists() -> bool:
        return postgresdblayer.allTablesExists()

    def setupDb(drop_schema : bool, create_schema : bool, populate_data : bool):
        return postgresdblayer.setupDb(drop_schema, create_schema, populate_data)