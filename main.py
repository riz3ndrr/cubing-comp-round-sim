import requests

RESULTS = 'results'


id = "2019RAMO05"
url = f"https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/persons/{id}.json"
response = requests.get(url)
times = []
num_results = 0
if response.status_code == 200:
    data = response.json()
    for comp, results in data[RESULTS].items():
        if '333' in results:
            for result in results['333']:
                print(result['solves'])
                for solve in result['solves']:
                    times.append(solve) 
                num_results += 1
                if num_results == 5:
                    break
else:
    print(f"Request failed with status code {response.status_code}")


print(times)
