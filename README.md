![ParanoidInstaller](/art/paranoidinstaller.jpg)
##### An easy-to-use, plug-and-play AOSPA installer.
Language: Python 3.8.x <br>
Platform: Linux/Windows/macOS
```
/*
 * I'm not responsible for bricked devices, dead SD cards, thermonuclear war, or you getting fired because the alarm app failed. 
 * Please do some research if you have any concerns about features included in the products you find here before flashing it! 
 * YOU are choosing to make these modifications, and if you point the finger at me for messing up your device, I will laugh at you. 
 * Your warranty will be void if you tamper with any part of your device / software.
 */
```
### Installation:
- Install Google Platform Tools from ![here](https://developer.android.com/studio/releases/platform-tools) to PATH.
- Clone this repository to your desired location.
``` 
git clone https://github.com/gaganmalvi/ParanoidInstaller aospainstall
```
- Install Android SDK tools on Linux/macOS (we already ship Windows executables.) A simple Google search can help you out.
- If you have not installed Python yet, install Python 3.8.x or above on your PC.
- Before running the command below, make sure to install all requirements by running:
```
pip3 install -r requirements.txt
```
- Run the following command to run the Python script:
```
python3 aospainstall/main.py
```

### Features:
- ROMs, ZIP installer (works with any recovery that supports ADB sideload)
- Easy recovery installer
- Ability to download files with your specified URLs

##### If you like my work, please consider donating. 
###### Support email: malvi@aospa.co
