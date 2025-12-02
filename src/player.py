from numpy import random, clip
import csv
import requests
import pandas as pd
import os
from constants import DNF, MO3_EVENTS, SPRINT_EVENTS
NUM_RESULTS_TO_COLLECT = 50
INVALID_TIMES = [-1, -2, 0]


class PlayerHasNoResultsError(Exception):
    """Exception raised when a player has no results for a given event"""
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code 
    def __str__(self):
        return f"{self.message} (Error Code: {self.error_code})"

class InvalidWCAIDError(Exception):
    """Exception raised when the inputted WCA ID does not exist"""
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code 
    def __str__(self):
        return f"{self.message} (Error Code: {self.error_code})"


class Player:
    def calcBPAandWPA(self):
        times = self.times[:4]

        self.bpa = (sum(times) - max(times)) / 3
        if DNF in times:
            self.wpa = DNF
        else:
            self.wpa = (sum(times) - min(times)) / 3
        #return bpa, wpa
    def calcProvisionalMean(self):
        self.provisionalMean = (self.times[0] + self.times[1]) / 2

class UserPlayer(Player):
    def __init__(self, name, event):
        self.name = name
        self.avg = None
        self.times = []
        self.wpa = 0 
        self.bpa = 0
        self.event = event
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
        if self.event in MO3_EVENTS:
            if num_dnf > 0:
                self.avg = DNF 
            else:
                self.avg = total / 3 
        else:
            if num_dnf > 1:
                self.avg = DNF 
            else:
                self.avg = (total - fastest - slowest) / 3
    def updateCSV(self, placing, num_ppl):
        filename = f"../data/{self.event}.csv"
        # If Filename does NOT exist
        if os.path.exists(filename) is False:
            with open(filename, 'w') as players_csv:
                num_times = 3 if self.event in MO3_EVENTS else 5  
                headers = [f"t{x + 1}" for x in range(num_times)] + ["average", "placing", "num_ppl"]
                csvwriter = csv.writer(players_csv)
                csvwriter.writerow(headers)

        with open(filename, 'a') as players_csv:
            csvwriter = csv.writer(players_csv)
            data_to_append = [self.times[x] for x in range(len(self.times))]
            data_to_append.append(self.avg)
            data_to_append.append(placing)
            data_to_append.append(num_ppl)
            csvwriter.writerow(data_to_append)

class GennedPlayer(Player):
    def __init__(self, wca_id, event):
        self.wca_id = wca_id
        url = f"https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/persons/{self.wca_id}.json"
        self.response = requests.get(url) 
        self.event = event
        if self.validPlayer() is False:
            raise InvalidWCAIDError("Invalid WCA ID", 400)
        else:
            self.player_data = self.response.json()
            self.name = self.player_data['name']
            self.country = self.player_data['country']
            self.rank, self.pr_avg = self.findAvgStats()
            self.pr_sin = self.findSinStats()
            self.avg, self.times = self.generateNewResults()
            #TODO MAKE THIS EFFICIENT
            self.mo50_recent = self.calculate_mean_of_50_recent_solves()
            self.calcBPAandWPA()
            self.calcProvisionalMean() 
    
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
                            if solve not in INVALID_TIMES:
                                times.append(solve) 
                                num_results += 1
                            if num_results == NUM_RESULTS_TO_COLLECT:
                                return times
            if len(times) == 0 :
                raise PlayerHasNoResultsError("Player has no results in this event", 400)
            return times
        else:
            print(f"Request failed with status code {self.response.status_code}")

    def calcNormalDistribution(self, times, nd_size):
        result = []
        if times is None:
            return result
        
        std = 1 if self.event not in SPRINT_EVENTS else 0.6
        dist = random.normal(loc = sum(times) / len(times) / 100, scale = std, size = nd_size)
        dist = clip(dist, 0.5, None)
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
        num_solves_to_generate = 3 if self.event in MO3_EVENTS else 5

        for _ in range(num_solves_to_generate):
            new_time = random.choice(data_nd)
            if new_time == DNF:
                num_dnf += 1
            times.append(new_time)
        
        total = sum(times)
        fastest = min(times)
        slowest = max(times)

        if num_solves_to_generate == 3:
            if num_dnf > 0:
                avg = DNF 
            else:
                avg = total / 3 
        else:
            if num_dnf > 1:
                avg = DNF 
            else:
                avg = (total - fastest - slowest) / 3

        return avg, times

