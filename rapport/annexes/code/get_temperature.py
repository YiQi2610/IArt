import re
def get_temperature(path):
    temp_list = []
    with open(path, 'r') as f:
        line = f.readline()
        while(line!=""):           
            match = re.search(r'\d+\.\d+', line)
            temp_list.append(float(match.group()))
            line = f.readline()
    temperature = max(temp_list)
    return temperature
