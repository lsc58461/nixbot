import configparser

from ftplib import FTP
from Now_Time import Time


config = configparser.ConfigParser()

def FTP_Post(FileName_PatchNote):
    try:
        ftp = FTP('nixserver.dothome.co.kr')
        ftp.login("nixserver", "dlswb4fkd!")
        
        ftp.cwd('html/DATA')  # 업로드할 FTP 폴더로 이동
        myfile = open(FileName_PatchNote,'rb')  # 로컬 파일 열기
        print(f"{Time()})  FTP 로컬 파일 열기 완료")
        ftp.storbinary('STOR ' +FileName_PatchNote, myfile )  # 파일을 FTP로 업로드
        print(f"{Time()})  FTP 업로드 완료")
        myfile.close()  # 파일 닫기
        print(f"{Time()})  FTP 파일 닫기 완료")
        ftp.quit()
        print(f"{Time()})  FTP 모듈 종료")
        try:
            config['Data'] = {}
            config['Data']['Detect'] = '1'
            with open("Detect.ini", 'w', encoding='UTF-8-SIG') as configfile:
                config.write(configfile)
                print(f"{Time()})  Detect.ini 완료")
        except:
            print(f"{Time()})  Detect.ini 파일 쓰기 실패")
            return None
        return
    except:
        return 
