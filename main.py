# Copyright (C) 2020 Paranoid Android
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import urllib.request as r
import subprocess
import json
from tqdm import tqdm
from collections import OrderedDict 

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def downloadFile(url, output_path, silent = False):
    if silent:
        r.urlretrieve(url, filename=output_path)
    else:
        print('Beginning download...')
        with DownloadProgressBar(unit='B', unit_scale=True,
                                 miniters=1, desc=url.split('/')[-1]) as t:
            r.urlretrieve(url, filename=output_path, reporthook=t.update_to)

def getDeviceCodename():
    result = subprocess.run(['adb', 'shell', 'getprop', 'ro.product.vendor.device'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return result.strip()

def isAbDevice():
    result = subprocess.run(['adb', 'shell', 'getprop', 'ro.boot.slot_suffix"'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return result.strip() is not None

def getPaDevices():
    devices = OrderedDict()
    dl = 'http://api.aospa.co/devices'
    downloadFile(dl,'devices.json', True)
    with open("devices.json") as f:
        djson = json.load(f)
        for i in range(len(djson["devices"])):
            devices[djson["devices"][i]["name"]] = djson["devices"][i]["description"]
    
    return devices
    
def downloadLatestRelease(codename):
    dl = 'http://api.aospa.co/updates/'+codename
    downloadFile(dl,'pa.json', True)
    with open('pa.json') as f:
        device = json.load(f)
        try: event = max(device['updates'], key=lambda ev: ev['version'])
        except ValueError:
            paDevices = getPaDevices()
            print("Codename %s not found in PA releases! We support the following devices:" % codename)
            for i in range(len(paDevices)):
                codename = list(paDevices.items())[i][0]
                print(" [%d] %s - %s" % (i+1, codename, paDevices[codename]))
            try: chosen = int(input("Choose your device or hit enter to exit: ")) - 1
            except ValueError: exit()
            if chosen not in range(len(paDevices)):
                print("Invalid choice!")
                exit()
            else:
                downloadLatestRelease(list(paDevices.items())[chosen][0])
        downloadURL = event.get('url')
        print('Downloading latest PA release...')
        downloadFile(downloadURL,'pa.zip')

def FastbootInstall():
    print('Device connected:',getDeviceCodename())
    print('You are going to install Paranoid Android via fastboot, any changes made are irreversible!')
    x = input('Do you wish to continue? [Y/N]')
    if x.capitalize() == 'Y':
        print('Rebooting to fastboot...')
        subprocess.run(['adb', 'reboot', 'bootloader'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        input('Press return when the device has rebooted to bootloader')
        subprocess.run(['fastboot','update','rom.zip'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        print('ROM successfully flashed.')
        input('Press return to reboot to system.')
        rsubprocess.run(['fastboot', 'reboot'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        Intro()
    else:
        print('Wrong option.')
        Intro()

def ROMInstall():
    print('Device connected:',getDeviceCodename())
    downloadLatestRelease(getDeviceCodename())
    print('THIS ACTION WILL POTENTIALLY BREAK AND DELETE PARTITIONS AND ITS CONTENTS. DO YOU WANT TO CONTINUE?')
    x = input('Are you sure to continue? (Y/N)')
    if x.capitalize() == 'Y':
        print('Running ROM installation, do not unplug your device or power it off.')
        result = subprocess.run(['adb', 'reboot', 'sideload-auto-reboot'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(result)
        input('Once you see device rebooting to recovery, press enter.')
        result = subprocess.run(['adb', 'sideload', 'pa.zip'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(result)
        print('ROM successfully sideloaded.')
        Intro()
    else:
        Intro()

def LocalROMInstall():
    print('Device connected:',getDeviceCodename())
    print('Save the ROM zip in the root directory of the installer as pa.zip')
    print('THIS ACTION WILL POTENTIALLY BREAK AND DELETE PARTITIONS AND ITS CONTENTS. DO YOU WANT TO CONTINUE?')
    x = input('Are you sure to continue? (Y/N)')
    if x.capitalize() == 'Y':
        print('Running ROM installation, do not unplug your device or power it off.')
        result = subprocess.run(['adb', 'reboot', 'sideload-auto-reboot'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(result)
        print('STORE THE ROM ZIP IN THE DIRECTORY OF THE SCRIPT, OTHERWISE THE SCRIPT WILL FAIL.')
        input('Once you see device rebooting to recovery, press enter.')
        result = subprocess.run(['adb', 'sideload', 'pa.zip'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(result)
        print('ROM successfully sideloaded.')
        Intro()
    else:
        Intro()


def RcvryInstall():
    print('The device is: ',getDeviceCodename())
    print('THIS ACTION WILL POTENTIALLY BREAK AND DELETE PARTITIONS AND ITS CONTENTS. DO YOU WANT TO CONTINUE?')
    x = input('Are you sure to continue? (Y/N)')
    if x.capitalize() == 'Y':    
        print('Running Recovery installation, do not unplug your device or power it off')
        result = subprocess.run(['adb', 'reboot', 'bootloader'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        input('Once device has reached bootloader state, press enter to continue')
        if isAbDevice():
            recovery_partition = 'boot'
        else:
            recovery_partition = 'recovery'
        result = subprocess.run(['fastboot', 'flash', recovery_partition, 'recovery.img'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        print('Booting to system...')
        result = subprocess.run(['fastboot', 'reboot'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        print('Booting...')
        Intro()
    else:
        Intro()

def Intro():
    print('=====================')
    print('  ParanoidInstaller')
    print('=====================\n')
    print('The easiest way to get Paranoid Android on your device!\n')
    print('Device:',getDeviceCodename())
    print('Select your choice:\n')
    print(' [1] Install Paranoid Android using the Internet.')
    print(' [2] Install Paranoid Android from local ZIP.')
    print(' [3] Install Paranoid Android Recovery.')
    print(' [4] Exit')
    userInput = int(input('Enter your selection: '))
    if userInput == 1:
        ROMInstall()
    elif userInput == 2:
        LocalROMInstall()
    elif userInput == 3:
        print('Store recovery IMG as recovery.img in root directory of the script.')
        input('Press any key to continue...')
        RcvryInstall()
    elif userInput == 4:
        x = input('Are you sure to exit? (Y/N)')
        if x.capitalize() == 'Y':
            exit()
        else:
            Intro()
    else:
        Intro()

print('''
                                                                                
                                                                                
          .(%%%%((%%    .#%%%%#.    ,#%%%%%(. ,((*/((((*      *((((/*((.        
         %%%*   *%%%  *%%#.  .%%%* #%%        ,(((.   *((/  (((*   .(((.        
        #%%.     (%%  %%%      #%%  #%%%%%%/  ,((,     ,((.,((,     ,((.        
        .%%%.   .%%%  (%%(    #%%/  ,    .%%% ,((/    ,(((  (((,    (((.        
          *%%%%%%#%%    /%%%%%%/   /%%%%%%%/  ,((/(((((/     .((((((/((.        
                                              ,((,                              
                                                                                
                                                                                 \n''')
Intro()


    
