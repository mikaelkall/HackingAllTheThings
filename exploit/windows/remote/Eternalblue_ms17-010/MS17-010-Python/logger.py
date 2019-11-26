from time import gmtime, strftime
red = "\033[1;31m"
blue = "\033[1;34m"
yellow = "\033[1;33m"
green = "\033[1;32m"
orange = "\033[33m"


greenbg = "\033[42;1m"
redbg = "\033[41;1m"
remove = "\033[0m"

spacing="\t"

def RED(string): return (red + string + remove)
def BLUE(string): return (blue + string + remove)
def YELLOW(string): return (yellow + string + remove)
def GREEN(string): return (green + string + remove)
def ORANGE(string): return (orange + string + remove)

def GREENBG(string): return (greenbg + string + remove)
def REDBG(string): return (redbg + string + remove)

def info(string):
	cur_time=strftime("%H:%M:%S", gmtime())
	print(BLUE("[{}]  [INFO]: ".format(cur_time)) + spacing + string)

def action(string):
	cur_time=strftime("%H:%M:%S", gmtime())
	print(YELLOW("[{}]  [ACTION]: ".format(cur_time)) + spacing + string)

def alert(string):
	cur_time=strftime("%H:%M:%S", gmtime())
	print(ORANGE("[{}]  [ALERT]: ".format(cur_time)) + spacing + string)

def error(string):
	cur_time=strftime("%H:%M:%S", gmtime()) 
	print(RED("[{}]  [ERROR]: ".format(cur_time)) + spacing + string)

def success(string):
	cur_time=strftime("%H:%M:%S", gmtime()) 
	print(GREEN("[{}]  [SUCCESS]: ".format(cur_time)) + spacing + string)

def target(string):
	cur_time=strftime("%H:%M:%S", gmtime())  
	# print (GREENBG(string))
	print(GREENBG("[{}]  [TARGET]:{}{}".format(cur_time,spacing,string)))
