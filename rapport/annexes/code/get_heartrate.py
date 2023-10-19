def get_heartrate(path):
    with open(path, 'r') as f:
        heartrate = f.readline()
    return heartrate