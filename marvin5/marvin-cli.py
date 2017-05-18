#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example to show how command-line options can be handled by a script.
"""



import sys
import os
from datetime import datetime
import getopt
import requests
from bs4 import BeautifulSoup




#
# Add some stuff about this script
#
PROGRAM = os.path.basename(sys.argv[0])
AUTHOR = "Dennis Özturk"
EMAIL = "dennis.dada@hotmail.se"
VERSION = "1.1.0"
USAGE = """{program} - Print my name. By {author} ({email}), version {version}.
Usage:
  {program} [options] name
Options:
  -h, --help                         Display this help message.
  -v, --version                      Print version and exit.
  -s, --silent                       Do not display any details or statistics
                                     about the execution.
  -p, --ping                         Ping a Website
  -d <number>, --drums=<number>      Make a drum sound when writing the name.
  -r <number>, --repeat=<number>     Print the name several times.
  -o <filename>, --output=<filename> Save output to file.

  name                               Your name.
""".format(program=PROGRAM, author=AUTHOR, email=EMAIL, version=VERSION)

MSG_VERSION = "{program} version {version}.".format(program=PROGRAM, version=VERSION)
MSG_USAGE = "Use {program} --help to get usage.\n".format(program=PROGRAM)




#
# Global default settings affecting behaviour of script in several places
#
REPEAT = 0
DRUM = 0
SILENT = False
VERBOSE = True
NAME = ""
OUTPUT = None

EXIT_SUCCESS = 0
EXIT_USAGE = 1
EXIT_FAILED = 2


def ping(second):
    """ ping a website """
    url = str(second)
    req = requests.head(url)

    print("Request to ", url)
    print("Recieved status code: ", req.status_code)

    exit()

def history(second):
    """ content of website """
    response = requests.get(second)
    print(response.content)

    exit()
def save(link):
    """Saves information """
    response = requests.get(link)
    content = str(response.content)
    f = open("humans.txt", 'a+')
    f.write(content)
    f.close()

def quote():
    """prints out daily quoute """
    print(__doc__)
    input("Press enter to continue. ")


    url = "http://dbwebb.se/javascript/lekplats/get-marvin-quotes-using-ajax/quote.php"


    try:

        print("\nReady to send HTTP request to ", url, "\nPress enter to continue. ", end='')
        input()
        req = requests.get(url)

        print("\nThe response status code is:\n", req.status_code)

        print("\nThe response body is:\n", req.text)

        json = req.json()
        print("\nQuote of today is:\n\"{quote}\"\n".format(quote=json["quote"]))


    except requests.ConnectionError:

        print("Failed to connect.")
def title(info):
    """ Title of a website """
    r = requests.get(info)
    # Get the text of the contents
    html_content = r.text

    # Convert the html content into a beautiful soup object
    soup = BeautifulSoup(html_content, 'html.parser')
    print(soup.title)
def printUsage(exitStatus):
    """
    Print usage information about the script and exit.
    """
    print(USAGE)
    sys.exit(exitStatus)



def printVersion():
    """
    Print version information and exit.
    """
    print(MSG_VERSION)
    sys.exit(EXIT_SUCCESS)



def printMyName():
    """
    Print the name.
    """

    msg = "My name is "

    if DRUM:
        msg += NAME[0:1] * DRUM

    msg += NAME
    msg += NAME * REPEAT
    msg += "!"
    print(msg)

    if OUTPUT:
        if VERBOSE:
            print("Saving output to file: ", OUTPUT)

        with open(OUTPUT, "w") as f:
            f.write(msg + "\n")



def parseOptions():
    """
    Merge default options with incoming options and arguments and return them as a dictionary.
    """
    # Switch through all options
    try:
        global DRUM, REPEAT, VERBOSE, OUTPUT, NAME

        opts, args = getopt.getopt(sys.argv[1:], "hvsd:r:o:", [
            "help",
            "version",
            "silent",
            "history",
            "ping=",
            "drum=",
            "repeat=",
            "output="
        ])

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                printUsage(EXIT_SUCCESS)

            elif opt in ("-v", "--version"):
                printVersion()

            elif opt in ("-s", "--silent"):
                VERBOSE = False

            elif opt in ("-d", "--drum"):
                if not arg.isnumeric():
                    assert False, "-d, --drum: {arg} is not a numeric value".format(arg=arg)

                DRUM = int(arg)

                if VERBOSE:
                    print("Setting DRUM to ", DRUM)

            elif opt in ("-r", "--repeat"):
                if not arg.isnumeric():
                    assert False, "-r, --repeat: {arg} is not a numeric value".format(arg=arg)

                REPEAT = int(arg)

                if VERBOSE:
                    print("Setting REPEAT to ", REPEAT)

            elif opt in ("-o", "--output"):
                OUTPUT = arg

                if VERBOSE:
                    print("Setting OUTPUT to ", OUTPUT)

            else:
                assert False, "Unhandled option"

        if len(args) != 1:
            assert False, "Missing name as argument"

        # The name passed as a required argument
        NAME = args[0]

    except Exception as err:
        print(err)
        print(MSG_USAGE)
        # Prints the callstack, good for debugging, comment out for production
        # traceback.print_exception(Exception, err, None)
        sys.exit(EXIT_USAGE)




def main():
    """
    Main function to carry out the work.
    """
    """
    a = sys.argv[1]
    b = sys.argv[2]
    ping(a,b)
    """

    startTime = datetime.now()

    parseOptions()

    printMyName()

    timediff = datetime.now()-startTime
    if VERBOSE:
        sys.stderr.write("Script executed in {}.{} seconds\n".format(timediff.seconds, timediff.microseconds))

    sys.exit(EXIT_SUCCESS)



if __name__ == "__main__":
    a = sys.argv[1]
    if(a == "ping"):
        b = sys.argv[2]
        ping(b)
    elif(a == "get"):
        b = sys.argv[2]
        history(b)
    elif(a == "quote"):
        quote()
    elif(a == "title"):
        b = sys.argv[2]
        title(b)
    elif("--output=" in a):
        b = sys.argv[2]
        c = sys.argv[3]
        save(c)
    else:
        main()
