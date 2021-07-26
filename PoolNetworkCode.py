class Pool(object):
    def __init__(self, name):
        self.name = name
        self._NE_list = []

    '''
        This API is used to add a network-element level to the pool
    '''
    #It would be good to create header like this for all API's
    def AddNetworkElementInPool(self, NEID):
        if NEID in self._NE_list:
            print("Network element {} already in pool {}.".format(NEID.name, self.name))
            return -1
        else:
            #Add the NE to the Pool
            self._NE_list.append(NEID)
            
            #Associate the PoolID with NE also for easy access
            NEID.poolID = self
            
            return 0
        
    '''
        This API is used to del a network-element level from the pool
    '''
    def DelNetworkElementInPool(self, NEID):
        if NEID in self._NE_list:
            NED.poolID = None
            del self._NE_list[self._NE_list.index(NEID)]
            return 0
        else:
            print("Network Element {} not in pool {}".format(NEID.name, self.name))
            return -1

    '''
        This API is used to display the poolID + all the NE's in the Pool
    '''
    def ShowNetworkElementsInPool(self):
        print("Pool ID: " + self.name)
        print('NEs in Pool: ', end='')
        for NE in self._NE_list:
            print(NE.name + ',', end= '')
        #for new line 
        print('')    

class NetworkElement(object):
    def __init__(self, name):
        self.name = name
        self._password = "admin"
        self.poolID = None
        self.APN_list = []

    def Login(self):
        if input("Password: ") == self._password:
            return True
        return False

    def changePassword(self, old_password, new_password):
        #Didn't get this part
        if old_password == self._password:
            self._password = new_password
        else:
            print("Access denied")
            
    def ExecuteCLI(self, CLI):
        self.Login()
        
    def  ShowDetails(self):
        #shows details of NE, poolID, neighbor NE in same pool
        print("NE-Name  :" + self.name)
        poolID = self.poolID
        print("Pool ID: " + poolID.name)
        print('Neighbour NEs : ', end='')
        for NE in poolID._NE_list:
            if NE != self:
                print(NE.name + ',', end= '')
        #for new line 
        print('')   
            
    def AssociateAPN(self, APN):
        if APN in self._APN_list:
            print("APN {} already associated with NE {}".format(APN.name, NE.name))
            return -1
        else:
            #Associate the APN to NE
            self._APN_list.append(APN)
            return 0
         
    def DissociateAPN(self, APN):
        if APN in self._APN_list:
            self._APN_list.remove(APN)
            return 0
        else:
            print("APN {} not associated with NE {}".format(APN.name, NE.name))
            return -1

class AccessPoint(object):
    def __init__(self, name):
        self.name = name
        #by default state is UP (1), DOWN(0)
        self.state = 1
    
    def UpdateState(self, state):
         self.state = state 

class MonitorElement(object):
    def __init__(self, name):
        self.name = name

    def SetAlarm(NEID, APN):
        pass
    def ClearAlarm(NEID, APN):
        pass

def main():
    NE1=NetworkElement("NE1")
    NE2=NetworkElement("NE2")
    Pool1 = Pool("Pool1")
    Pool1.AddNetworkElementInPool(NE1)
    Pool1.AddNetworkElementInPool(NE1)
    #Pool1.ShowNetworkElementsInPool()
    #NE1.ShowDetails()
    #NE2.ShowDetails()


if __name__ == '__main__':
    main()

