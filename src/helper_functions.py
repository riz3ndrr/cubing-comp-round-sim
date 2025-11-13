def convertToReadableTime(inputted_time):
    if inputted_time < 60:
        return f"{inputted_time:.2f}"
    min, sec = divmod(inputted_time, 60)
    if sec < 10:
        return (f"{min:.0f}:0{sec:.2f}")
    return (f"{min:.0f}:{sec:.2f}")
