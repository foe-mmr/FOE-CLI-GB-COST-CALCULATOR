# FOE Command Line GB Cost Calculator

File foe_snipe.py contains Python script that can be used to calculate if GB is profitable for sniping

1. First Clone or download repository or you can simply copy foe_snipe.py content and create new file. You will also need TextFormatter.py in same directory.

2. Install (if not already installed) pip for Python 2 with:

```
sudo apt install python-pip
```
3. To install pychrome and tabulate, simply:

```
pip install pychrome
```

```
pip install tabulate
```

4. Setup Chrome with debugging (chrome version >= 59):

If on Linux or MacOS you can use:

```
python open_chrome.py
```

that will open new chrome session with debuggind mode and you will not have to close all chrome windows. (Tested only on MacOS but shopuld work on Linux too)

```
google-chrome --remote-debugging-port=9222
```

Or for OSX:

```
/Applications/Google\ Chrome\ 2.app/Contents/MacOS/Google\ Chrome  --remote-debugging-port=9222
```

No other Chrome windows should be open before. Chrome window should be opened automatically after running this command.

5. In another terminal run python script:
```
python foe_snipe.py
```

6. open FOE in browser and if everythings ok then you should see something like this in terminal:

```
ARC bonus:  90 %
Open GB to use calculator
```

after you have opened some GB:

```
#    Cost    Difference
---  ------  ------------
1    0       0
2    73      5
3    0       0
4    0       0
5    0       0
Remaining FPs to level:  75
INVEST:  73
REWARD:  5
```

Its totally safe to use as only server request responses are read, theres no way for Inno to know that you are using this.

## How to install and run Python on Windows

1. download Python 2.7 installer https://www.python.org/downloads/windows/
2. Install Python
3. Open Command line: Start menu -> Run and type cmd.
4. Install pip:
	for Python 2.7.9+ type:
  ```
	C:\python27\python.exe py -3 -m ensurepip
  ```
5. install pychrome and tabulate:
  ```
	C:\Python27\Scripts\pip.exe install pychrome
  ```
  and
  
  ```
	C:\Python27\Scripts\pip.exe install tabulate
  ```

6. Type to run script. change "YOUR-USER-NAME" to your actuall username or change path if you have downloaded it elsewhere : 
  ```
	C:\python27\python.exe C:\Users\YOUR-USER-NAME\Downloads\FOE-CLI-GB-COST-CALCULATOR-master\foe_snipe.py
  ```
