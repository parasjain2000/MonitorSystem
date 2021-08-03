import sys
VERBOSE = 0

class AccessPoint(object):
    def __init__(self, name: str):
        self.name = name
        print_verbose("Created APN: {}".format(name))

class NetworkElement(object):
    def __init__(self, name: str):
        self.name = name
        self._password = "admin"
        self.poolID = None
        self._APN_list = []
        self.down_APNs = []
        print_verbose("Created NE: {}".format(name))

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
            print("Pool ID: " + self.poolID.name)
            print('Neighbour NEs: ', end='')
            for NE in self.poolID._NE_list:
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
        print_verbose("Associating NE {} to APN {}".format(self.name, APN.name))
        return 0
         
    def DissociateAPN(self, APN: AccessPoint) -> int:
        '''Dissociates the network element with an access point.
        
        If the dissociation is successful, returns 0. If the access point is not already assocciated, returns -1.
        '''
        
        #Dissociates the access point if it is associated.
        if APN in self._APN_list:
            print_verbose("Disssociating NE {} to APN {}".format(self.name, APN.name))
            self._APN_list.remove(APN)
            return 0

        #Alerts the user if the access point is not already associated with the pool.
        print("APN {} not associated with NE {}".format(APN.name, NE.name))
        return -1
    
class Pool(object):
    def __init__(self, name: str):
        self.name = name
        self._NE_list = []
        print_verbose("Created Pool : {}".format(name))

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
        print_verbose("Associating NE {} to Pool {}".format(NEID.name, self.name))

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
        
        #For new line 
        print('\n')    

class MonitorElement(object):
    def __init__(self, name: str):
        self.name = name
        print_verbose("Created Monitoring System: {}".format(name))

    def SetAlarm(self, NEID: NetworkElement, APN: AccessPoint) -> None:
        '''Tells all the other network elements in the pool that this network element has reported this access point as down.'''
        
        print_verbose("Set Alarm from NE {} for APN {}..".format(NEID.name, APN.name))
        #Log in to other network elements in pool and make note that this network element has reported this access point as down.
        for NE in NEID.poolID._NE_list:
            if NE != NEID and NE.Login("admin"):
                print_verbose("Login to NE {} to SET (NE: {}, APN {})..".format(NE.name, NEID.name, APN.name))
                NE.down_APNs.append([NEID, APN])
        print_verbose("DONE...................\n\n")
    
    def ClearAlarm(self, NEID: NetworkElement, APN: AccessPoint) -> None:
        '''Removes the notice sent by "MonitorElement.SetAlarm".'''
        
        print_verbose("Clear Alarm from NE {} for APN {}..".format(NEID.name, APN.name))
        #Log in to other network elements in pool and remove notice that this network element has reported this access point as down.
        for NE in NEID.poolID._NE_list:
            if NE != NEID and NE.Login("admin"):
                print_verbose("Login to NE {} to CLEAR (NE: {}, APN {})..".format(NE.name, NEID.name, APN.name))
                NE.down_APNs.pop([NEID, APN])
        print_verbose("DONE...................\n\n")

def print_verbose(info):
    if VERBOSE == 1:
        print(info)

def main():
    global VERBOSE
    if len(sys.argv) == 2:
        args = sys.argv[1:]
        option = args[0]
        if option == '-v':
            VERBOSE=1

    print_verbose("Creating NE's 1 to 6...")
    NE1 = NetworkElement("NE1")
    NE2 = NetworkElement("NE2")
    NE3 = NetworkElement("NE3")
    NE4 = NetworkElement("NE4")
    NE5 = NetworkElement("NE5")
    NE6 = NetworkElement("NE6")
    print_verbose("DONE...................\n\n")
   
    print_verbose("Creating NE's 1 to 5...")
    Pool1 = Pool("Pool1")
    Pool2 = Pool("Pool2")
    Pool3 = Pool("Pool3")
    print_verbose("DONE...................\n\n")
    
    print_verbose("Creating APNs...")
    APN1 = AccessPoint("fastinternet.com")
    APN2 = AccessPoint("greatservice.com")
    APN3 = AccessPoint("provider.org")
    print_verbose("DONE...................\n\n")
    
    Monitor = MonitorElement("Monitoring Element")
    print_verbose("DONE...................\n\n")
    
    print_verbose("Creating Associations...")
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
    print_verbose("DONE...................\n\n")
    
    Monitor.SetAlarm(NE1, APN1)
    Monitor.SetAlarm(NE2, APN1)
    #Monitor.ClearAlarm(NE1, APN1)

    '''
    Pool1.ShowNetworkElementsInPool()
    Pool2.ShowNetworkElementsInPool()
    Pool3.ShowNetworkElementsInPool()
   
    NE1.ShowDetails()
    NE2.ShowDetails()
    NE3.ShowDetails()
    NE4.ShowDetails()
    NE5.ShowDetails()
    NE6.ShowDetails()
    '''


if __name__ == '__main__':
    main()
