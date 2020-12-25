'''
Copyright (C) 2020 Gagan Malvi
Licensed under the Cartel Project Public License available at
https://github.com/CartelProject/CPL
All rights reserved
I am hereby NOT responsible for any damage caused whatsoever by this tool
and you're solely responsible because you decided to use it in the first 
place. So if you scream at me, I will laugh at you.
'''

import os

def ROMInstall():
    print('Running ROM installation, do not unplug your device or power it off.')
    os.system('adb reboot sideload')
    os.system('adb sideload rom.zip')
    print('ROM successfully sideloaded, if the device does not reboot, manually reboot to system.')
    Intro()

def RcvryInstall():
    print('Running Recovery installation, do not unplug your device or power it off')
    os.system('adb reboot-bootloader')
    os.system('fastboot flash recovery recovery.img')
    userInput = input('Do you want to boot to recovery or proceed to reboot to system? [Y/N]')
    if userInput.capitalize() == "Y":
        print('Booting to recovery...')
        os.system('fastboot boot recovery.img')
        print('Successfully booted to recovery.')
    elif userInput.capitalize() == "N":
        print('Booting to system...')
        os.system('fastboot reboot')
        print('Successfully booted to system.')
    else:
        print('Wrong choice.')
    Intro()

def Intro():
    print('====================')
    print('Cartel ROM Installer')
    print('====================\n')
    print('A simple ROM installer for Android devices that are supported by the Cartel Project.\n')
    print('Select your choice:\n')
    print(' [1] Install Cartel ROM.')
    print(' [2] Install a compatible recovery.')
    # TODO: DOWNLOAD FILES AUTOMATICALLY
    print(' [3] Exit')
    userInput = int(input('Enter your selection [1/2/3]:'))
    if userInput == 1:
        print('Store ROM zip as rom.zip in the root directory of the script.')
        input('Press any key to continue...')
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

Intro()



    
