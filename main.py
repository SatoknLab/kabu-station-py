from src.kabucom import Kabucom
from pprint import pprint
from getpass import getpass
import os

def load_api_password():
    password = os.getenv("KABUCOM_API_PASSWORD_PREVIEW")
    if password is None:
        password = getpass("Input API Password: ")
    return password

password = load_api_password()
kabucom = Kabucom("development")
kabucom.authorize(password)
pprint(kabucom.get_soft_limit())
pprint(kabucom.get_wallet_cash())