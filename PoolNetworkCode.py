class Pool(object):
    def __init__(self, name):
        self.name = name
        self.NE_list = []

    def AddNetworkElementInPool(self, NEID):
        self.NE_List.append(NEID)

    def DelNetworkElementInPool(self, NEID):
        pass 

class NetworkElement(object):
    def __init__(self, name):
        self.name = name
        APN_list = []

    def Login(self):

    def ExecuteCLI(self, CLI):
        self.Login()

  
  
class AccessPoint(object):
    def __init__(self, name):
        self.name = name
    
    Def UpdateState(self, State):
         Self.state = state 

class MonitorElement(object):
    def __init__(self, name):
        self.name = name

    Def SetAlarm(NEID, APN):
      
    Def ClearAlarm(NEID, APN):
