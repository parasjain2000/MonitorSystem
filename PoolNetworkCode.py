import sys
VERBOSE = 0
from collections import defaultdict
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
        print_fail("Incorrect password. Access denied.")
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
            print_fail("Incorrect password.")
            
    def ExecuteCLI(self, CLI):
        self.Login()
        
    def ShowDetails(self, prestr : str) -> None:
        '''Displays details about the network element.
        
        Information displayed includes the network element's ID, its associated pool, the other network elements in the pool, and the assocciated access points.
        '''
        
        #Prints the NEID.
        print(prestr + "NE-Name: " + self.name)
        
        #Will not report any poolID of neighbor network elements if this network element is not in a pool.
        if self.poolID == None:
            print(prestr + "Not associated with a pool.")
        else:
            print(prestr + "Associated Pool ID: " + self.poolID.name)
            print(prestr + 'Neighbour NEs: ', end='')
            for NE in self.poolID._NE_list:
                if NE != self:
                    print(NE.name + ',', end= '')
            #print('\n')
            print('Associated APNs: ', end='')
            for APN in self._APN_list:
                print(APN.name + ',', end= '')
        #For new line.
        #print runtime APN status
        if len(self.down_APNs) != 0:
            print('')
            print(prestr+"Runtime Status : ")
            print(prestr + "Received SetAlarm for :", end = '')
            for NE,APN in self.down_APNs:
                print("( " + NE.name + " , " + APN.name + " )", end='') 
        
        #For new line.
        print('\n')

    def AssociateAPN(self, APN: AccessPoint) -> int:
        '''Associates the network element with an access point.
        
        If the association is successful, returns 0. If the access point is already assocciated, returns -1.
        '''
        
        #Alerts the user if the access point is already associated.
        if APN in self._APN_list:
            print_fail("APN {} already associated with NE {}".format(APN.name, self.name))
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
        print_fail("APN {} not associated with NE {}".format(APN.name, NE.name))
        return -1
    
class Pool(object):
    def __init__(self, name: str):
        self.name = name
        self._NE_list = []
        self._APN_down_NEs = defaultdict(list)  #Stores the NE's which have declared this APN as down
        print_verbose("Created Pool : {}".format(name))

    def AddNetworkElementInPool(self, NEID: NetworkElement) -> int:
        '''Adds a network element to the pool.
        
        If the addition is successful, returns 0. If the network element is already in the pool, returns -1.
        '''
        #If the network element is already in the pool, print a message alerting the user.
        if NEID in self._NE_list:
            print_fail("Network element {} already in pool {}.".format(NEID.name, self.name))
            return -1
        
        #If the network element is already in the some other pool, print a message alerting the user.
        if NEID.poolID != None:
            print_fail("Network element {} already in pool {}.".format(NEID.name, NEID.poolID.name))
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
        print_fail("Network Element {} not in pool {}".format(NEID.name, self.name))
        return -1

    def ShowNetworkElementsInPool(self, prestr:str) -> None:
        '''Displays the poolID and all the network elements in the pool.'''
        
        print(prestr + "Printing details of Pool ID: " + self.name)
        print(prestr + 'NEs in Pool: ')
        for NE in self._NE_list:
            #print(NE.name + ',', end= '')
            NE.ShowDetails("{}    ".format(prestr))
        if len(self._APN_down_NEs) != 0:
            print(prestr+"Runtime Status :")
            for Key in self._APN_down_NEs:
                print(prestr+"  " + Key + "  : ", end = '')
                for NE in self._APN_down_NEs[Key]:
                    print(NE.name + ", ", end = '')
            print()
        print()


class MonitorElement(object):
    def __init__(self, name: str, pools):
        self.name = name
        self.pools = pools
        print_verbose("Creating Monitoring System: {}".format(name))

    def SetAlarm(self, NEID: NetworkElement, APN: AccessPoint) -> None:
        '''Tells all the other network elements in the pool that this network element has reported this access point as down.'''
        
        print_verbose("Set Alarm from NE {} for APN {}..".format(NEID.name, APN.name))
        pool = NEID.poolID
        if type(NEID) != NetworkElement or type(APN) != AccessPoint or type(pool) != Pool:
            print_fail("Invalid arguments NEID {}, APN {}, pool {}".format(NEID, APN, pool))
            return -1

        #check if NE's is associated to that APN
        if APN not in NEID._APN_list:
            print_fail("NE {} not associated with APN {}".format(NEID.name, APN.name))
            return -1

        #Key is the APN + Pool Name
        Key = pool.name+":"+APN.name

        #check if the APN already exists as down by some other NE
        if Key in pool._APN_down_NEs:
            if NEID in pool._APN_down_NEs[Key]:
                print_fail("Network Element {} already declared APN {} down, duplicate/ignoring".format(NEID.name, APN.name))
                return 0
        pool._APN_down_NEs[Key].append(NEID)

        #check if it is the last NE in pool to delcare it down
        if len(pool._APN_down_NEs[Key]) == len(pool._NE_list):
            print_fail("Last NE {} in Pool {} to declare APN {} Down, do nothing".format(NEID.name, pool.name, APN.name))
            return 0

        count = 0
        #Log in to other network elements in pool and make note that this network element has reported this access point as down.
        for NE in NEID.poolID._NE_list:
            if NE != NEID and APN in NE._APN_list:
                count += 1
                if NE.Login("admin"):
                    print_verbose("Login to NE {} to SET (NE: {}, APN {})..".format(NE.name, NEID.name, APN.name))
                    NE.down_APNs.append([NEID, APN])

        if count == 0:
            print_fail("Last NE {} in Pool {} to declare APN {} Down, do nothing".format(NEID.name, pool.name, APN.name))
            return 0

        print_verbose("DONE...................\n\n")
    
    def ClearAlarm(self, NEID: NetworkElement, APN: AccessPoint) -> None:
        '''Removes the notice sent by "MonitorElement.SetAlarm".'''
        
        print_verbose("Clear Alarm from NE {} for APN {}..".format(NEID.name, APN.name))
        pool = NEID.poolID
        Key = pool.name+":"+APN.name

        #check if the APN already exists as down by some other NE
        if Key not in pool._APN_down_NEs:
            print_fail("APN {} Alarm already cleared for all NE's, duplicate/ignoring".format(NEID.name, APN.name))
            return 0

        if NEID not in pool._APN_down_NEs[Key]:
            print_fail("Network Element {} already declared APN {} Up, duplicate/ignoring".format(NEID.name, APN.name))
            return 0

        pool._APN_down_NEs[Key].remove(NEID)
        #Log in to other network elements in pool and remove notice that this network element has reported this access point as down.
        for NE in NEID.poolID._NE_list:
            if NE != NEID and NE.Login("admin"):
                print_verbose("Login to NE {} to CLEAR (NE: {}, APN {})..".format(NE.name, NEID.name, APN.name))
                NE.down_APNs.remove([NEID, APN])
        print_verbose("DONE...................\n\n")


    def showSystem(self, prestr:str):
        print(prestr+"Display Monitoring system details...")
        for pool in self.pools:
            pool.ShowNetworkElementsInPool("{}    ".format(prestr))
        print(prestr+"DONE...................\n\n")


def print_verbose(info):
    if VERBOSE == 1:
        print(info)

def print_fail(msg):
    print(bcolors.FAIL+msg+bcolors.ENDC)

def main():
    global VERBOSE
    if len(sys.argv) == 2:
        args = sys.argv[1:]
        option = args[0]
        if option == '-v':
            VERBOSE = 1

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
   
    pools = [Pool1, Pool2, Pool3]
    Monitor = MonitorElement("Monitoring Element", pools)
    print_verbose("DONE...................\n\n")
    
    print_verbose("Creating Associations...")
    Pool1.AddNetworkElementInPool(NE1)
    Pool1.AddNetworkElementInPool(NE3)
    
    Pool2.AddNetworkElementInPool(NE5)
    
    Pool3.AddNetworkElementInPool(NE2)
    Pool3.AddNetworkElementInPool(NE4)
    Pool3.AddNetworkElementInPool(NE6)
    
    NE1.AssociateAPN(APN1)
    NE1.AssociateAPN(APN2)
    NE3.AssociateAPN(APN1)
    
    NE5.AssociateAPN(APN1)
    NE5.AssociateAPN(APN2)
    
    NE2.AssociateAPN(APN1)
    NE2.AssociateAPN(APN3)
    NE4.AssociateAPN(APN3)
    NE6.AssociateAPN(APN2)
    NE6.AssociateAPN(APN3)
    print_verbose("DONE...................\n\n")
   
    Monitor.SetAlarm(NE1, APN1)
    Monitor.SetAlarm(NE5, APN1)
    Monitor.SetAlarm(NE2, APN1)
    Monitor.ClearAlarm(NE1, APN1)
    '''Monitor.SetAlarm(NE3, APN1)
    Monitor.SetAlarm(NE1, APN1)'''

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
