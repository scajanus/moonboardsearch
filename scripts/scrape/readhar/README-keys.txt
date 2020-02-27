Problem keys
============

Method - feet follows, etc
Name - Name of climb (mostly ALLCAPS it seems)
Grade - Font Grade
UserGrade - IGNORE
MoonBoardConfiguration: <-- is None for 2016 set
  Description - 40° MoonBoard or 25° MoonBoard
  HighGrade -  always None
  Id - 1 for 40 degree, 2 for 25 degree
  LowGrade  - always None

MoonBoardConfigurationId - always 0
Setter:
    Id - long ID wih hyphens
    Firstname 
    Lastname
    Nickname - Can include spaces
    City 
    Country
    ProfileImageUrl - url from website (can be  default profile png or user jpg)
    CanShareData - True or False
FirstAscender - IGNORE (is the user the first to ascend)
Rating - IGNORE all ratings were 0
UserRating - IGNORE Users Rating
Repeats - int repeats
Attempts - IGNORE (User attempts)
Holdsetup:
    Active - Is active flag (none are marked as Active)
    AllowClimbMethods - ?? IGNORE (never on active holdsetup)
    DateDeleted - UNUSED
    DateInserted - UNUSED
    DateUpdated - UNUSED
    Description - "Moonboard Masters 2019" - states the obvious but some are wrong
    HoldLayoutId - Always 0
    Holdsets - Always None
    Id - (15 when description is 2017, 17 when description is 2019)
    IsLocked - UNUSED
    MoonBoardConfigurations - Always None
    Setby - always None

IsBenchmark - is benchmark
IsMaster - (only  20) (moonboard masters)
IsAssessmentProblem - (only 32 occurences)
ProblemType - IGNORE? Only a few values recorded 'Crimp', 82 // 'Dynamic', 11
Moves: a list of dicts
   Description -  rowid e.g. G5
   Id -  uniqueid
   IsEnd - is end hold
   IsStart -  is start hold

Holdsets - IGNORE ?? All  Values None
Locations - position and rotation of holds
RepeatText - 'Be the first to repeat this problem' or 'N  climbers have repeated this problem'
NumberOfTries - IGNORE (how many tries the user has had before succeeding)
NameForUrl - Hyphenated lower case version of name
Upgraded  -  Whether user upgraded?
Downgraded - Whether user downgraded?
Id - Unique ID (up to 370,000 etc)
ApiId - IGNORE
DateInserted  - UnixTimestamp
DateUpdated  -  IGNORE
DateDeleted - IGNORE
DateTimeString - User Friendly Time Created

Example

{'ApiId': 0,
 'Attempts': 0,
 'DateDeleted': None,
 'DateInserted': '/Date(1582533936337)/',
 'DateTimeString': '24 Feb 2020 08:45',
 'DateUpdated': None,
 'Downgraded': False,
 'FirstAscender': False,
 'Grade': '6B+',
 'Holdsets': None,
 'Holdsetup': {'Active': False,
               'AllowClimbMethods': True,
               'DateDeleted': None,
               'DateInserted': None,
               'DateUpdated': None,
               'Description': 'MoonBoard Masters 2019',
               'HoldLayoutId': 0,
               'Holdsets': None,
               'Id': 17,
               'IsLocked': False,
               'MoonBoardConfigurations': None,
               'Setby': None},
 'Id': 364020,
 'IsAssessmentProblem': False,
 'IsBenchmark': False,
 'IsMaster': False,
 'Locations': [{'Color': '0x0000FF',
                'Description': None,
                'Direction': 0,
                'DirectionString': 'N',
                'HoldNumber': None,
                'Holdset': None,
                'Id': 0,
                'Rotation': 0,
                'Type': 0,
                'X': 195,
                'Y': 338},
               {'Color': '0x0000FF',
                'Description': None,
                'Direction': 0,
                'DirectionString': 'N',
                'HoldNumber': None,
                'Holdset': None,
                'Id': 0,
                'Rotation': 0,
                'Type': 0,
                'X': 245,
                'Y': 586},
               ...
               {'Color': '0x00FF00',
                'Description': None,
                'Direction': 0,
                'DirectionString': 'N',
                'HoldNumber': None,
                'Holdset': None,
                'Id': 0,
                'Rotation': 0,
                'Type': 0,
                'X': 595,
                'Y': 688}],
 'Method': 'Feet follow hands',
 'MoonBoardConfiguration': {'Description': '40° MoonBoard',
                            'HighGrade': None,
                            'Id': 1,
                            'LowGrade': None},
 'MoonBoardConfigurationId': 0,
 'Moves': [{'Description': 'G5',
            'Id': 2089465,
            'IsEnd': False,
            'IsStart': True},
           {'Description': 'K6',
            'Id': 2089466,
            'IsEnd': False,
            'IsStart': True},
           ...
           {'Description': 'H18',
            'Id': 2089472,
            'IsEnd': True,
            'IsStart': False}],
 'Name': 'MARKING MY TILES',
 'NameForUrl': 'marking-my-tiles',
 'NumberOfTries': None,
 'ProblemType': None,
 'Rating': 0,
 'RepeatText': 'Be the first to repeat this problem',
 'Repeats': 0,
 'Setter': {'CanShareData': True,
            'City': 'Singapore',
            'Country': 'SINGAPORE',
            'Firstname': 'Choo',
            'Id': '1a874be7-4d04-457e-aee4-fde87e006765',
            'Lastname': 'Wei Chen wilson',
            'Nickname': 'Wilsonchooweichen',
            'ProfileImageUrl': '/Content/Account/Images/default-profile.png?637181326655694758'},
 'Upgraded': False,
 'UserGrade': None,
 'UserRating': 0}
