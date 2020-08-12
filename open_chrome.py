from sys import platform
import subprocess
from subprocess import call

def main():
	myCmd = False

	if platform == "linux" or platform == "linux2":
	    myCmd = 'RND_DIR=/tmp/$RANDOM; google-chrome --remote-debugging-port=9222 --user-data-dir=$RND_DIR; rm -R $RND_DIR'
	    subprocess.call(myCmd,shell=True)
	elif platform == "darwin":
	    myCmd = 'RND_DIR=/tmp/$RANDOM; /Applications/Google\ Chrome\ 2.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=$RND_DIR; rm -R $RND_DIR'
	    subprocess.call(myCmd,shell=True)
	elif platform == "win32":
	    # Windows...
	    print "please try to figure out how to run this on Windows"

if __name__ == '__main__':
	main()
	raw_input()