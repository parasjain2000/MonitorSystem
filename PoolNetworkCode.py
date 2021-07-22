class Pool(object):
    def __init__(self, name):
        self.name = name
        self._NE_list = []

    def AddNetworkElementInPool(self, NEID):
        if NEID in self._NE_list:
            print("Network element already in pool.")
            
        else:
            self._NE_list.append(NEID)

    def DelNetworkElementInPool(self, NEID):
        if NEID in self._NE_list:
            del self._NE_list[self._NE_list.index(NEID)]
    
    def ShowNetworkElementsInPool(self):
        for NE in self.NE_list:
            print("NE.name")

class NetworkElement(object):
    def __init__(self, name):
        self.name = name
        self._password = "admin"
        self.APN_list = []

    def Login(self):
        if input("Password: ") == self._password:
            return True
        
        return False

    def changePassword(self, old_password, new_password):
        if old_password == self._password:
            self._password = new_password
        
        else:
            print("Access denied")
            
    def ExecuteCLI(self, CLI):
        self.Login()
        
class AccessPoint(object):
    def __init__(self, name):
        self.name = name
    
    def UpdateState(self, State):
         Self.state = state 

class MonitorElement(object):
    def __init__(self, name):
        self.name = name

    def SetAlarm(NEID, APN):
        pass
    def ClearAlarm(NEID, APN):
        pass
