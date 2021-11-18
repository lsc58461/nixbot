import configparser

Config = configparser.ConfigParser()

def Config_Detect():
    Config.read('Detect.ini', encoding='UTF-8-SIG') 
    Config.sections()
    Detect = int(Config['Data']['Detect'])
    return Detect

def Config_Title():
    Config.read('Data.ini', encoding='UTF-8-SIG') 
    Config.sections()
    Title = Config['Data']['Title']
    return Title