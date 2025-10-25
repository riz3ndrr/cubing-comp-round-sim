from numpy import random
import requests
NUM_RESULTS_TO_COLLECT = 50
DNF = 999

class Player:
    def calcBPAandWPA(self):
        times = self.times[:4]

        self.bpa = (sum(times) - max(times)) / 3
        if DNF in times:
            self.wpa = DNF
        else:
            self.wpa = (sum(times) - min(times)) / 3
        #return bpa, wpa

class UserPlayer(Player):
    def __init__(self, name):
        self.name = name
        self.avg = None
        self.times = []
        self.wpa = 0 
        self.bpa = 0

    def addTime(self, new_time):
        self.times.append(new_time)
    
    def generateAvg(self):
        num_dnf = 0
        for num in self.times:
            if num == DNF:
                num_dnf += 1

        total = sum(self.times)
        fastest = min(self.times)
        slowest = max(self.times)

        if num_dnf > 1:
            self.avg = DNF
        else:
            self.avg = (total - fastest - slowest) / (3)



class GennedPlayer(Player):
    def __init__(self, wca_id, event):
        self.wca_id = wca_id
        url = f"https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/persons/{self.wca_id}.json"
        self.response = requests.get(url) 
        self.event = event
        if self.validPlayer():
            self.player_data = self.response.json()
            self.name = self.player_data['name']
            self.country = self.player_data['country']
            self.rank, self.pr_avg = self.findAvgStats()
            self.pr_sin = self.findSinStats()
            self.avg, self.times = self.generateNewResults()
            #TODO MAKE THIS EFFICIENT
            self.mo50_recent = self.calculate_mean_of_50_recent_solves()
            self.calcBPAandWPA()


    
    
    def findAvgStats(self):
        for event_info in self.player_data['rank']['averages']:
            if self.event == event_info['eventId']:
                return event_info['rank']['world'], event_info['best'] / 100
        return None, None

    def findSinStats(self):
        for event_info in self.player_data['rank']['singles']:
            if self.event == event_info['eventId']:
                return event_info['best'] / 100

    def __str__(self):
        return f"{self.name}, WCA ID: {self.wca_id}"
    
    def __repr__(self):
        return self.__str__()

    def validPlayer(self):
        return self.response.status_code == 200

    def calculate_mean_of_50_recent_solves(self):
        recent_results = self.getRecentResults()
        result = []
        i = 0
        while i < 50 and len(recent_results) > 0:
            result.append( (recent_results.pop() / 100) )
            i += 1
        return sum(result) / len(result)
    
    def getRecentResults(self):
        num_results = 0
        times = []
        if self.validPlayer():
            for comp, results in self.player_data['results'].items():
                if self.event in results:
                    for result in results[self.event]:
                        for solve in result['solves']:
                            if solve != DNF:
                                times.append(solve) 
                                num_results += 1
                            if num_results == NUM_RESULTS_TO_COLLECT:
                                return times
            return times
        else:
            print(f"Request failed with status code {self.response.status_code}")

    def calcNormalDistribution(self, times, nd_size):
        result = []
        if times is None:
            return result
        dist = random.normal(loc = sum(times) / len(times) / 100, scale = 1, size = nd_size)
        # Having 2 guaranteed DNFs is completely arbitrary
        dnf_indices = range(2)
        # Allows for scalability if I want more DNFs in the data set
        dist[dnf_indices] = DNF
        return dist

    def generateNewResults(self):
        recent_results = self.getRecentResults()
        data_nd = self.calcNormalDistribution(recent_results, 98)
        
        times = []
        
        num_dnf = 0
        for _ in range(5):
            new_time = random.choice(data_nd)
            if new_time == DNF:
                num_dnf += 1
            times.append(new_time)
        
        total = sum(times)
        fastest = min(times)
        slowest = max(times)

        if num_dnf > 1:
            avg = DNF
        else:
            avg = (total - fastest - slowest) / (3)
        return avg, times

