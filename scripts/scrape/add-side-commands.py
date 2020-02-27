# idpatternexample  = "1051c047-3e12-4da7-a937-87b5338dc8ac"
import random
from string import Template
import math

board = '2016'
numproblems = 29320

board = '2017'
numproblems = 30843

board = '2019'
numproblems = 1791

numpages = math.ceil(numproblems/15)
# Get a len length random hex string
def gethex(len):
    return str(hex(random.randint(0, pow(16,len))))[2:]

# Get an id for each selenium action
def getid():
    return "%s-%s-%s-%s-%s"%(gethex(8),gethex(4),gethex(4),gethex(4),gethex(12))


# Get template parts
repeater =  Template(open('moonboard.side-repeater').read())
header = open('moonboard%s.side-header'%board).read()
footer = open('moonboard.side-footer').read()


mapping = dict()
# Print template results to screen
print(header)
for n in range(14,numpages,3):

    mapping['id1'] = getid()
    mapping['num1'] = n
    mapping['lichild1'] = 4
    mapping['contains1'] = 7

    mapping['id2'] = getid()
    mapping['num2'] = n+1
    mapping['lichild2'] = 5
    mapping['contains2'] = 8

    mapping['id3'] = getid()
    mapping['num3'] = n+2
    mapping['lichild3'] = 6
    mapping['contains3'] = 9

    print(repeater.substitute(mapping))

print(footer)
