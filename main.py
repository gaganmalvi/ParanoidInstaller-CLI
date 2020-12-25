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

def downloadFile(link, path):
    print('Beginning download of ROM...')
    r.urlretrieve(link, path)

def getDeviceCodename():
    result = subprocess.run(['adb', 'shell', 'getprop', 'ro.build.product'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return result

def readCodeName():
    f = open("properties.cartel")
    return(f.read())

def FastbootROMFlash():
    print('Current device: ',getDeviceCodename())
    print('THIS ACTION WILL POTENTIALLY BREAK AND DELETE PARTITIONS AND ITS CONTENTS. IT MIGHT RENDER YOUR DEVICE UNUSABLE IF YOU DO SOMETHING WRONG.')
    print('THIS FUNCTION WILL ONLY WORK ON A-ONLY DEVICES!')
    print('MAKE SURE YOU HAVE THE CORRECT IMAGES, CHECK CODENAMES BEFORE FLASH.')
    x = input('Are you sure to continue? (Y/N)')
    if x.capitalize() == 'Y':
        print('Running ROM installation, do not unplug your device or power it off.')
        result = subprocess.run(['adb','reboot','bootloader'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(result)
        input('Press enter if you are sure to continue with the process. THE CHANGES MADE ARE IRREVERSIBLE.')
        subprocess.run(['fastboot', 'flash', 'boot', 'boot.img'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        subprocess.run(['fastboot', 'flash', 'recovery', 'recovery.img'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        subprocess.run(['fastboot', 'flash', 'system', 'system.img'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        subprocess.run(['fastboot', 'flash', 'system', 'vendor.img'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        print('ROM successfully flashed via fastboot, if the device does not reboot, manually reboot to system.')
        Intro()
    else:
        Intro()
        
def ROMInstall():
    getDeviceCodename()
    print('THIS ACTION WILL POTENTIALLY BREAK AND DELETE PARTITIONS AND ITS CONTENTS. DO YOU WANT TO CONTINUE?')
    x = input('Are you sure to continue? (Y/N)')
    if x.capitalize() == 'Y':
        print('Running ROM installation, do not unplug your device or power it off.')
        result = subprocess.run(['adb', 'reboot', 'sideload'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(result)
        print('STORE THE ROM ZIP IN THE DIRECTORY OF THE SCRIPT, OTHERWISE THE SCRIPT WILL FAIL.')
        input('Once you see device rebooting to recovery, press enter.')
        name = input('Enter ROM zip filename: ') # Should be saved as rom.zip if it is downloaded by the downloadFile function
        result = subprocess.run(['adb', 'sideload', name], stdout=subprocess.PIPE).stdout.decode('utf-8')
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
    print('====================')
    print('Cartel ROM Installer')
    print('====================\n')
    print('A simple ROM installer for Android devices that are supported by the Cartel Project.\n')
    print('Device: ',getDeviceCodename())
    print('Select your choice:\n')
    print(' [1] Install Cartel ROM.')
    print(' [2] Install a compatible recovery.')
    print(' [3] Download Cartel ROM from a mirror of your choice.')
    print(' [4] Install Cartel ROM via Fastboot images. ')
    # TODO: Download files automatically by checking the codename of the device using getDeviceCodename()
    print(' [5] Exit')
    userInput = int(input('Enter your selection:'))
    if userInput == 1:
        ROMInstall()
    elif userInput == 2:
        print('Store recovery IMG as recovery.img in root directory of the script.')
        input('Press any key to continue...')
        RcvryInstall()
    elif userInput == 3:
        url = input('Enter URL of file: ')
        path = 'rom.zip'
        downloadFile(url,path)
    elif userInput == 4:
        FastbootROMFlash()
    elif userInput == 5:
        x = input('Are you sure to exit? (Y/N)')
        if x.capitalize() == 'Y':
            exit()
        else:
            Intro()
    else:
        Intro()

print('''/¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\\
|                   O                   |
| |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯| |
| |                                   | |
| |				      | |
| |                                   | |
| |                                   | |
| |                                   | |
| |                                   | |
| |                                   | |
| |                                   | |
| |                                   | |
| |                                   | |
| |                                   | |
| |               Cartel              | |
| |              Installer            | |
| |                                   | |
| |                                   | |
| |                                   | |
| |                                   | |
| |                                   | |
| |                                   | |
| |                                   | |
| |                                   | |
| |                                   | |
| |                                   | |
| |                                   | |
| |                                   | |
| |___________________________________| |
|					|
|     <             O		 =	|
\_______________________________________/ \n''')
Intro()


    
