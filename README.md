# FOE Command Line GB Cost Calculator

File foe_snipe.py contains Python script that can be used to calculate if GB is profitable for sniping

1. First Clone or download repository or you can simply copy foe_snipe.py content and create new file. You will also need TextFormatter.py in same directory.

2. Install (if not already installed) pip for Python 2 with:

```
sudo apt install python-pip
```
3. To install pychrome, simply:

```
pip install pychrome
```

4. Setup Chrome headless mode (chrome version >= 59):

```
google-chrome --headless --disable-gpu --remote-debugging-port=9222
```

Or for OSX:

```
/Applications/Google\ Chrome\ 2.app/Contents/MacOS/Google\ Chrome  --remote-debugging-port=9222
```

No other Chrome windows should be open before. Chrome window should be opened automatically after running this command and in it open the FOE world for which you would like to create MMR table. Once game is done loading

5. In another terminal run python script:
```
python foe_snipe.py
```

If everythings ok then you should see something like this in terminal after you have opened some GB:
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

At the moment this works only for GBs that you dont already have a fps invested.

Its totally safe to use as only server request responses are read, theres no way for Inno to know that you are using this.
