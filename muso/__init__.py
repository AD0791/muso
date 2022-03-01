from requests import get
from requests.auth import HTTPBasicAuth
from pandas import DataFrame
""" from cachetools import (
    cached,
    TTLCache
) """

from muso.settings import setting

__version__ = '0.2.0'
__app_name__ = "Muso"


# cache = TTLCache(maxsize=10000, ttl=86400)

_oauth = HTTPBasicAuth(setting.email_comcare,setting.password_comcare)

#@cached(cache)
def form_bd():
    pay = {'xmlns':setting.xmlns, 'limit':setting.limit}
    forms = get(setting.form_base_url,auth=_oauth,params=pay).json()
    __objects = forms["objects"]
    __meta = forms["meta"]
    

    while __meta["next"]:
        __forms = get(f"""{setting.form_base_url}{__meta['next']}""",auth=_oauth).json()
        __objects += __forms["objects"]
        __meta = __forms["meta"]
    
    return __objects

#@cached(cache)
def form_ibd():
    pay_cases = {'type':setting.types,'limit':setting.caselimit}
    form_cases = get(setting.case_base_url,auth=_oauth,params=pay_cases).json()
    __objects_cases = form_cases["objects"]
    __meta_cases = form_cases["meta"]

    while __meta_cases["next"]:
        __form_cases = get(f"""{setting.case_base_url}{__meta_cases['next']}""",auth=_oauth).json()
        __objects_cases += __form_cases["objects"]
        __meta_cases = __form_cases["meta"]
    
    return __objects_cases



_bd = DataFrame(list(
    map(
        lambda k: {
            "userID":k['metadata']['userID'],
            "username":k['metadata']['username'],
            "timeEnd": k['metadata']['timeEnd'],
            "case_id": k['form']['case']['@case_id'],
            "houseold_number_2022": k['form']['household_number'],
            "db_name": k['form']['nom'],
            "db_first_name": k['form']['prenom']
        } 
        ,form_bd()
    )
))
_bd.drop_duplicates('case_id',inplace=True)
_bd.reset_index(drop=True)
__bd = _bd.head(1000)

_ibd = DataFrame(list(
    map(
        lambda k: {
            "userID": k['user_id'],
            "ib_case_id": k['case_id'],
            "age": k['properties']['age'],
            "sexe": k['properties']['sexe'],
            "arv": k['properties']['arv'],
            "test": k['properties']['test'],
            "ib_case_id": k['case_id'],
            "parent_case_id": k['indices']['parent']['case_id'],
            "relationship": k['indices']['parent']['relationship'],
        } 
        ,form_ibd()
    )
))
__ibd = _ibd.head(1000)
