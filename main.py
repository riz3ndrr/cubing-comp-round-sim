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

    def validPlayer(self):
        return self.response.status_code == 200
 
    def getRecentResults(self, event):
        num_results = 0
        times = []
        if self.validPlayer():
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
        
NUM_PLAYERS = 8
player_list = []

while len(player_list) < NUM_PLAYERS:
    new_person_wca_id = input("Enter a person's WCA ID: ")

    if new_person_wca_id == "":
        break
    player_to_add = Player(new_person_wca_id)
    if player_to_add.validPlayer is False:
        print("ERROR")
    else:
        player_list.append(player_to_add)
print(player_list)



dwan = Player('2019RAMO05')
jasp = Player('2018MURR03')

times1 = dwan.calculateRound('333')
times2 = jasp.calculateRound('333')
print(times1)
print(times2)
