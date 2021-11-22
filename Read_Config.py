import configparser

Config = configparser.ConfigParser()

def Config_Title():
    Config.read('Data.ini', encoding='UTF-8-SIG') 
    Config.sections()
    Title = Config['Data']['Title']
    return Title
