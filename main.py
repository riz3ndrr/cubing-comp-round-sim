import requests
from pprint import pprint
from numpy import random


RESULTS = 'results'
NUM_RESULTS_TO_COLLECT = 50
DNF = 999
DNF_AVG = 999

def clear():
    print(chr(27) + "[2J")

class Player:
    def __init__(self, wca_id):
        
        self.avg = None
        self.times = None

    def validPlayer(self):
        return self.response.status_code == 200

    def __str__(self):
        return f"{self.name}, WCA ID: {self.wca_id}"
    def __repr__(self):
        return self.__str__()
    
    def printSinglesUpToSolveNum(self, solve_num):
        string = f"{self.name}: "
        for i in range(solve_num - 1):
            if self.times[i] == DNF:
                string += "DNF, "
            else:
                string += f"{self.times[i]:.2f}, "
        if self.times[solve_num - 1] == DNF:
            string += "DNF"
        else:
            string += f"{self.times[solve_num - 1]:.2f}"
        print(string)


class gennedPlayer(Player):
    def __init__(self, wca_id):
        self.wca_id = wca_id
        url = f"https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/persons/{self.wca_id}.json"
        self.response = requests.get(url) 
        if self.validPlayer():
            self.player_data = self.response.json()
            self.name = self.player_data['name']
        else:
            self.name = None

    def getRecentResults(self, event):
        num_results = 0
        times = []
        if self.validPlayer():
            for comp, results in self.player_data[RESULTS].items():
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

    def generateNewResults(self, event):
        recent_results = self.getRecentResults(event)
        data_nd = self.calcNormalDistribution(recent_results, 98)
        
        times = []
        
        num_dnf = 0
        for _ in range(5):
            new_time = random.choice(data_nd)
            if new_time == DNF:
                num_dnf += 1
            times.append(new_time)
        
        if num_dnf > 1:
            self.avg = DNF_AVG

        total = sum(times)
        fastest = min(times)
        slowest = max(times)
        self.avg = (total - fastest - slowest) / (3)
        self.times = times




NUM_PLAYERS = 8
EVENTS = [
    "222",      # 2x2x2 Cube
    "333",      # 3x3x3 Cube
    "444",      # 4x4x4 Cube
    "555",      # 5x5x5 Cube
    "666",      # 6x6x6 Cube
    "777",      # 7x7x7 Cube
    "333bf",    # 3x3x3 Blindfolded
    "333fm",    # 3x3x3 Fewest Moves
    "333oh",    # 3x3x3 One-Handed
    "333mbf",   # 3x3x3 Multi-Blind
    "pyram",    # Pyraminx
    "minx",     # Megaminx
    "skewb",    # Skewb
    "sq1",      # Square-1
    "clock",    # Rubik's Clock
    "444bf",    # 4x4x4 Blindfolded
    "555bf"     # 5x5x5 Blindfolded
]

def main():
    clear()
    player_list = []

    while len(player_list) < NUM_PLAYERS:
        new_person_wca_id = input("Enter a person's WCA ID: ")

        if new_person_wca_id == "":
            break
        player_to_add = gennedPlayer(new_person_wca_id)
        if player_to_add.validPlayer() is False:
            print("ERROR")
        else:
            player_list.append(player_to_add)

    clear()
    event = input("What event will you be competing in today? ")
    while event not in EVENTS:
        print("Invalid event")
        event = input("What event will you be competing in today? ")
    for player in player_list:
        player.generateNewResults(event)


    for i in range(5):
        clear()
        print("#" * 15, "SOLVE ", i + 1, " ", "#" * 15)

        player_list.sort(key = lambda x : min(x.times[:(i + 1)]))
        for player in player_list:
            player.printSinglesUpToSolveNum(i + 1)
        input()
    
    player_list.sort(key = lambda x : x.avg)
    for pos, player in enumerate(player_list):
        print(f"Position: {pos + 1} => {player.name}, Average = {player.avg:.2f}")

    

if __name__ == "__main__":
    main()
