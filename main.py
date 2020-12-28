'''
Copyright (C) 2020 Gagan Malvi
Licensed under the Cartel Project Public License available at
https://github.com/CartelProject/CPL
All rights reserved
I am hereby NOT responsible for any damage caused whatsoever by this tool
and you're solely responsible because you decided to use it in the first 
place. So if you scream at me, I will laugh at you.
'''

import urllib.request as r
import subprocess
import json

def downloadFile(link, path):
    print('Beginning download...')
    r.urlretrieve(link, path)

def getDeviceCodename():
    result = subprocess.run(['adb', 'shell', 'getprop', 'ro.build.product'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return result.strip()

def readCodeName():
    f = open("properties.cartel")
    return(f.read())

def downloadLatestRelease():
    dl = 'http://api.aospa.co/updates/'+getDeviceCodename()
    downloadFile(dl,'pa.json')
    with open('pa.json') as f:
        device = json.load(f)
        event = max(device['updates'], key=lambda ev: ev['version'])
        downloadURL = event.get('url')
        print('Downloading latest PA release...')
        downloadFile(downloadURL,'pa.zip')
        
def ROMInstall():
    print('Device connected:',getDeviceCodename())
    downloadLatestRelease()
    print('THIS ACTION WILL POTENTIALLY BREAK AND DELETE PARTITIONS AND ITS CONTENTS. DO YOU WANT TO CONTINUE?')
    x = input('Are you sure to continue? (Y/N)')
    if x.capitalize() == 'Y':
        print('Running ROM installation, do not unplug your device or power it off.')
        result = subprocess.run(['adb', 'reboot', 'sideload'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(result)
        print('STORE THE ROM ZIP IN THE DIRECTORY OF THE SCRIPT, OTHERWISE THE SCRIPT WILL FAIL.')
        input('Once you see device rebooting to recovery, press enter.')
        result = subprocess.run(['adb', 'sideload', 'pa.zip'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(result)
        print('ROM successfully sideloaded, if the device does not reboot, manually reboot to system.')
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
        result = subprocess.run(['fastboot', 'flash', 'recovery', 'recovery.img'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        userInput = input('Do you want to boot to recovery or proceed to reboot to system? [Y/N]')
        if userInput.capitalize() == "Y":
            print('Booting to recovery...')
            result = subprocess.run(['fastboot', 'boot', 'recovery.img'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            print(result)
            print('Successfully booted to recovery.')
        elif userInput.capitalize() == "N":
            print('Booting to system...')
            result = subprocess.run(['fastboot', 'reboot'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            print(result)
            print('Successfully booted to system.')
        else:
            print('Wrong choice.')
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
    print(' [1] Install Paranoid Android')
    print(' [2] Install PA Recovery')
    # TODO: Download files automatically by checking the codename of the device using getDeviceCodename()
    print(' [3] Exit')
    userInput = int(input('Enter your selection:'))
    if userInput == 1:
        ROMInstall()
    elif userInput == 2:
        print('Store recovery IMG as recovery.img in root directory of the script.')
        input('Press any key to continue...')
        RcvryInstall()
    elif userInput == 3:
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


    
