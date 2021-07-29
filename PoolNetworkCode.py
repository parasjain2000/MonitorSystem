class Pool(object):
    def __init__(self, name: str):
        self.name = name
        self._NE_list = []

    def AddNetworkElementInPool(self, NEID: NetworkElement) -> int:
        '''Adds a network element to the pool.
        
        If the addition is successful, returns 0. If the network element is already in the pool, returns -1.
        '''
        #If the network element is already in the pool, print a message alerting the user.
        if NEID in self._NE_list:
            print("Network element {} already in pool {}.".format(NEID.name, self.name))
            return -1
        
        #Add the NE to the Pool
        self._NE_list.append(NEID)

        #Associate the Pool with the network element for easy access.
        NEID.poolID = self

        return 0
        
    def DelNetworkElementInPool(self, NEID: NetworkElement) -> int:
        '''Deletes a network element from the pool.
        
        If the deletion is successful, returns 0. If the network element is not present in the pool to begin with, returns -1.
        '''
        
        #If the network element is in the pool, disassociates the network element from the pool.
        if NEID in self._NE_list:
            NEID.poolID = None
            del self._NE_list[self._NE_list.index(NEID)]
            return 0
        
        #Alerts the user if the network element is not in the pool.
        print("Network Element {} not in pool {}".format(NEID.name, self.name))
        return -1

    def ShowNetworkElementsInPool(self) -> None:
        '''Displays the poolID and all the network elements in the pool.'''
        
        print("Pool ID: " + self.name)
        print('NEs in Pool: ', end='')
        for NE in self._NE_list:
            print(NE.name + ',', end= '')
        #for new line 
        print('\n')    

class NetworkElement(object):
    def __init__(self, name: str):
        self.name = name
        self._password = "admin"
        self.poolID = None
        self._APN_list = []
        self.down_APNs = []

    def Login(self, password: str) -> bool:
        '''Returns "True" if the correct password is inputted, and returns "False" otherwise.
        
        Meant to be used by the monitoring element when using "MonitorElement.SetAlarm" and "MonitorElement.ClearAlarm."
        '''
        #Returns "True" if the inputted password is the same as the set password.
        if password == self._password:
            return True
        
        #Alerts the user if the password is incorrect.
        print("Incorrect password. Access denied.")
        return False

    def changePassword(self, old_password: str, new_password: str) -> None:
        '''Changes the network element's password.
        
        The new password will be used by "NetworkElement.Login."
        '''
        #The old password must be inputted correctly in order to change it.
        if old_password == self._password:
            self._password = new_password
            
        #Alerts the user if the old password was not inputted correctly.
        else:
            print("Incorrect password.")
            
    def ExecuteCLI(self, CLI):
        self.Login()
        
    def ShowDetails(self) -> None:
        '''Displays details about the network element.
        
        Information displayed includes the network element's ID, its associated pool, the other network elements in the pool, and the assocciated access points.
        '''
        
        #Prints the NEID.
        print("NE-Name: " + self.name)
        
        #Will not report any poolID of neighbor network elements if this network element is not in a pool.
        if self.poolID == None:
            print("Not associated with a pool.")
            
        else:
            poolID = self.poolID
            print("Pool ID: " + poolID.name)
            print('Neighbour NEs: ', end='')
            for NE in poolID._NE_list:
                if NE != self:
                    print(NE.name + ',', end= '')
                    
            #For new line.
            print('\n')
        
        
            
    def AssociateAPN(self, APN: AccessPoint) -> int:
        '''Associates the network element with an access point.
        
        If the association is successful, returns 0. If the access point is already assocciated, returns -1.
        '''
        
        #Alerts the user if the access point is already associated.
        if APN in self._APN_list:
            print("APN {} already associated with NE {}".format(APN.name, NE.name))
            return -1

        #Associates the access point to the network element.
        self._APN_list.append(APN)
        return 0
         
    def DissociateAPN(self, APN: AccessPoint) -> int:
        '''Dissociates the network element with an access point.
        
        If the dissociation is successful, returns 0. If the access point is not already assocciated, returns -1.
        '''
        
        if APN in self._APN_list:
            self._APN_list.remove(APN)
            return 0

        print("APN {} not associated with NE {}".format(APN.name, NE.name))
        return -1

class AccessPoint(object):
    def __init__(self, name: str):
        self.name = name

class MonitorElement(object):
    def __init__(self, name: str):
        self.name = name

    def SetAlarm(NEID: NetworkElement, APN: AccessPoint) -> None:
        for NE in NEID.poolID._NE_list:
            if NE != NEID and NE.Login():
                NE.down_APNs.append([NEID, APN])
    
    def ClearAlarm(NEID: NetworkElement, APN: AccessPoint) -> None:
        for NE in NEID.poolID._NE_list:
            if NE != NEID and NE.Login():
                NE.down_APNs.pop([NEID, APN])

def main():
    NE1 = NetworkElement("NE1")
    NE2 = NetworkElement("NE2")
    NE3 = NetworkElement("NE3")
    NE4 = NetworkElement("NE4")
    NE5 = NetworkElement("NE5")
    NE6 = NetworkElement("NE6")
    
    Pool1 = Pool("Pool1")
    Pool2 = Pool("Pool2")
    Pool3 = Pool("Pool3")
    
    APN1 = AccessPoint("fastinternet.com")
    APN2 = AccessPoint("greatservice.com")
    APN3 = AccessPoint("provider.org")
    
    Monitor = MonitorElement("Monitoring Element")
    
    Pool1.AddNetworkElementInPool(NE1)
    Pool1.AddNetworkElementInPool(NE3)
    
    Pool2.AddNetworkElementInPool(NE5)
    
    Pool3.AddNetworkElementInPool(NE2)
    Pool3.AddNetworkElementInPool(NE4)
    Pool3.AddNetworkElementInPool(NE6)
    
    NE1.AssociateAPN(APN1)
    NE3.AssociateAPN(APN1)
    
    NE5.AssociateAPN(APN2)
    
    NE2.AssociateAPN(APN3)
    NE4.AssociateAPN(APN3)
    NE6.AssociateAPN(APN3)
    
    Pool1.ShowNetworkElementsInPool()
    Pool2.ShowNetworkElementsInPool()
    Pool3.ShowNetworkElementsInPool()
    
    NE1.ShowDetails()
    NE2.ShowDetails()
    NE3.ShowDetails()
    NE4.ShowDetails()
    NE5.ShowDetails()
    NE6.ShowDetails()

if __name__ == '__main__':
    main()
