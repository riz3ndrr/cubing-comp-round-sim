def convertToReadableTime(inputted_time):
    if inputted_time < 60:
        return f"{inputted_time:.2f}"
    min, sec = divmod(inputted_time, 60)
    if sec < 10:
        return (f"{min:.0f}:0{sec:.2f}")
    return (f"{min:.0f}:{sec:.2f}")

def convertTimeStringToSec(inputted_time):
    # EXPECTING FORMAT min:sec:ms
    inputted_time = inputted_time.strip()
    times = inputted_time.split(":")
    try:
        if len(times) == 2:
            minutes, sec = times
            sec = float(sec) if sec else 0
        elif len(times) == 1:
            sec = float(times[0]) 
            minutes = 0
        else:
            return None

        result = float(minutes) * 60 + sec
        return result if result >= 0 else None 
    except ValueError:
        return None


# TESTING CONVERTING STRING TO SEC
#test_cases = [
#    "0:00.00", "0:01.00", "0:59.99", "1:00.00", "1:02.3", "2:30.50", "10:00.0",
#    "12:34.56", "0:5.1", "01:05.1", "00:00.1", "0:59", "5:00", "0.50", "1.22",
#    "59.99", "120.0", "360.45", "00:00", "00:59.999", "59:59.99", "99:59.99",
#    "0:0", "0", "", "abc", "1:", ":30", "1:2:3", "1:60", "-1:10", " 1:02.3 ", "1;02.3"
#]
#for t in test_cases:
#    try:
#        print(f"{t} -> {convertTimeStringToSec(t)}")
#    except Exception as e:
#        print(f"{t} -> Error: {e}")

