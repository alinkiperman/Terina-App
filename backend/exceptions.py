"""
@author: hadas lapid
all rights reserved
"""
import sys
import pandas as pd

# catch a specific error
try:
    pd.read_csv(hadas)
except NameError:
    x = input("give me file name\n")
    try:
        df = pd.read_csv(x)
    except FileNotFoundError:
        x = input("file does not exist, change file name\n")
        try:
            df = pd.read_csv(x)
        except:
            print(f"could not open file {x}")
        finally:
            print("Im done with you")

# catch as many errors as you wish:
try:
    df = pd.read_csv(filename)
    print(filename)
except NameError:
    filname = input("filename variable does not exist\n")
except FileNotFoundError:
    print(f"{filename} file was not found")
except:
    print("something else went wrong")

# you can pass the parts that went wrong and continue from there:
try:
    df = pd.read_csv(filename)
    print(filename)
except NameError:
    filname = input("filename variable does not exist\n")
finally:
    print("could not open file, continueing code")

# you can raise exceptions at your will:
x = input("insert number\n")

if not type(x) is int:
    raise TypeError("Only integers are allowed")

try:
    x = input("give me id number")
    for i in x:
        if not i.isnumeric():
            print(i)
            raise TypeError("Only integers are allowed in id")
except TypeError:
    print("got it!")
except BaseException as err:
    print(sys.exc_info()[0], err)

# get error info using sys.exc_info()[0]
try:
    f = open('myfile.txt')
    s = f.readline()
    i = int(s.strip())
except OSError as err:
    print(err, sys.exc_info()[0])