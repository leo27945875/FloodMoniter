import time
import datetime
import random
from iottalk import DAN


class Receiver(object):
    def __init__(self, serverURL, regAddr):
        Receiver.initFlag = True
        self.height = None
        self.serverURL = serverURL
        self.regAddr = regAddr
        self.profile = None

    def __repr__(self):
        site = super(Receiver, self).__repr__()

        return "\n"+"-"*50+"\n"+f"{site}\n"+'-'*50+f"\n{self.profile}"

    def ReceiveData(self, file, updateTime):
        DAN.profile['dm_name'] = 'FloodMoniter'
        DAN.profile['df_list'] = ['FloodHeightIn', 'FloodHeightOut']
        DAN.profile['d_name'] = 'FloodOutput'
        DAN.device_registration_with_retry(self.serverURL, self.regAddr)
        self.profile = DAN.profile
        with open(file, "a") as f:
            while True:
                try:
                    ODF_data = DAN.pull('FloodHeightOut')
                    if ODF_data != None:
                        now = datetime.datetime.now()
                        date = f"{now.year}/{now.month}/{now.day}"
                        clock = f"{now.hour}:{now.minute}:{now.second}"
                        self.height = ODF_data[0]
                        print(f"{self.height} cm")

                        f.write(f"{date},{clock},{self.height}\n")

                except Exception as e:
                    print(e)
                    if str(e).find('mac_addr not found:') != -1:
                        print('Reg_addr is not found. Try to re-register...')
                        DAN.device_registration_with_retry(
                            self.serverURL, self.regAddr)
                    else:
                        print('Connection failed due to unknow reasons.')
                        time.sleep(1)

                time.sleep(updateTime)
