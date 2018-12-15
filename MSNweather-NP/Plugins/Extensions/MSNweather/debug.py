from datetime import datetime
from os import path, system

def printDEBUG( myFUNC = '' , myText = '' ):
    try:
        from Components.config import config
        if config.plugins.WeatherPlugin.DebugEnabled.value:
            myDEBUGfile = '/tmp/MSNweather.log'
            print ("[%s] %s" % (myFUNC,myText))
            if myFUNC == 'INIT':
                f = open(myDEBUGfile, 'w')
            else:
                f = open(myDEBUGfile, 'a')
            f.write('[%s] %s%s\n' % (str(datetime.now()), myFUNC, myText))
            f.close
            if path.getsize(myDEBUGfile) > int(config.plugins.WeatherPlugin.DebugSize.value):
                system('sed -i -e 1,10d %s' % myDEBUGfile)
    except Exception:
        pass
