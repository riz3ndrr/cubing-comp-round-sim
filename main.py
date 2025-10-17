import requests

RESULTS = 'results'
NUM_RESULTS_TO_COLLECT = 50
DNF = -1

from numpy import random
import matplotlib.pyplot as plt


class Player:
    def __init__(self, wca_id):
        self.wca_id = wca_id
        url = f"https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/persons/{self.wca_id}.json"
        self.response = requests.get(url)
 
    def getRecentResults(self, event):
        num_results = 0
        times = []
        if self.response.status_code == 200:
            data = self.response.json()
            for comp, results in data[RESULTS].items():
                if event in results:
                    for result in results[event]:
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

    def calculateRound(self, event):
        recent_results = self.getRecentResults(event)
        data_nd = self.calcNormalDistribution(recent_results, 98)
        
        times = []
        print(data_nd)
        for _ in range(5):
            times.append(random.choice(data_nd))
        return times
        
    
    


dwan = Player('2019RAMO05')
jasp = Player('2018MURR03')

times1 = dwan.calculateRound('333')
times2 = jasp.calculateRound('333')
print(times1)
print(times2)
