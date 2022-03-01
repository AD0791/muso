from requests import get
from requests.auth import HTTPBasicAuth
from pandas import DataFrame


from muso.settings import setting

__version__ = '0.1.0'
__app_name__ = "Muso"


_oauth = HTTPBasicAuth(setting.email_comcare,setting.password_comcare)
_pay = {'xmlns':setting.xmlns, 'limit':setting.limit}
forms = get(setting.form_base_url,auth=_oauth,params=_pay).json()
__objects = forms["objects"]
__meta = forms["meta"]
#print(__meta)

while __meta["next"]:
    __forms = get(f"""{setting.form_base_url}{__meta['next']}""",auth=_oauth).json()
    __objects += __forms["objects"]
    __meta = __forms["meta"]


_pay_cases = {'type':setting.types,'limit':setting.caselimit}
form_cases = get(setting.case_base_url,auth=_oauth,params=_pay_cases).json()
__objects_cases = form_cases["objects"]
__meta_cases = form_cases["meta"]
#print(__meta_cases)

while __meta_cases["next"]:
    __form_cases = get(f"""{setting.case_base_url}{__meta_cases['next']}""",auth=_oauth).json()
    __objects_cases += __form_cases["objects"]
    __meta_cases = __form_cases["meta"]



__bd = DataFrame(list(
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
        ,__objects
    )
))
__bd.drop_duplicates('case_id',inplace=True)
__bd.reset_index(drop=True)


__ibd = DataFrame(list(
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
        ,__objects_cases
    )
))

