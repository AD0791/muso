from requests import get
from requests.auth import HTTPBasicAuth
from pandas import DataFrame, read_sql_query
import pymysql
from sqlalchemy import create_engine
""" from cachetools import (
    cached,
    TTLCache
) """

from musocapp.settings import setting

__version__ = '1.2.0'
__app_name__ = "musocapp"


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
__bd = _bd.head(100)

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
__ibd = _ibd.head(100)


_engine = create_engine(f"mysql+pymysql://{setting.user}:{setting.password}@{setting.hostname}/{setting.db}")

_query = f'''
SELECT
	au.username,
	au.email,
	count(*) as qty
FROM
	muso_household_2022 mh
	LEFT JOIN auth_users au ON mh.created_by = au.id
	group by au.username, mh.id_patient
'''

_muso_hiv = read_sql_query(_query,_engine,parse_dates=True)

_engine.dispose()

__hivmuso = _muso_hiv.groupby(['username','email']).count()
__hivmuso.loc['Total']= __hivmuso.sum(numeric_only=True, axis=0)
__hivmuso.reset_index(inplace=True)
