#### Prerequisite Script ####
## TO BE RAN BEFORE ANYTHING ELSE ##

try:
    import pip
    pip.main(['install','pyserial'])
    pip.main(['install','nidaqmx'])
    pip.main(['install','time'])
    pip.main(['install','pandas'])
    pip.main(['install','numpy'])
    pip.main(['install','matplotlib'])
    pip.main(['install','threading'])
    pip.main(['install','scipy'])
    pip.main(['install','sklearn'])

    print('Prerequisite Completed, you are now able to run the repository')

except ImportError as error:
    print(error.name)

