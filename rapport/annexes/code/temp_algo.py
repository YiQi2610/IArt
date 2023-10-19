# Cette fonction permet de trouver la température correspondante la plus proche
# parmi la liste [31, 31.5, 32, 32.5, 33, 33.5, 34, 34.5, 35, 35.5, 36, 36.5, 37, 37.5, 38]
def trouver_temp(T):

    a = 34.5

    if (T < 31.2):
        a = 31

    if (T > 37.7):
        a = 38
    
    L = [31.5, 32, 32.5, 33, 33.5, 34, 34.5, 35, 35.5, 36, 36.5, 37, 37.5]

    for newT in L:
        diff = abs(T-newT)
        if (diff <= 2.5):
            a = newT
    
    return a

# Cette fonction donne une liste de 4 mots décrivant brièvement l'état potentiel de la personne compte tenu de sa température faciale.
# Le premier mot indique si il est plus en hypo ou en hypertermie.
def liste_mots_temp(T):

    closerT = trouver_temp(T)
    L = []

    if(closerT == 31):
        L = ["Extremely cold", "Suffering", "Frigid"]
    elif (closerT == 31.5):
        L = ["Very cold", "Loneliness", "Numbing"]
    elif (closerT == 32):
        L = ["Very cold", "Grim", "Invigorating"]
    elif (closerT == 32.5):
        L = ["Cold", "Cosy", "Chilly"]
    elif (closerT == 33):
        L = ["Cold", "Peaceful", "Refreshing"]
    elif (closerT == 33.5):
        L = ["Mild", "Joyful", "Pleasant"]
    elif (closerT == 34):
        L = ["Mild", "Satisfaction", "Comfortable"]
    elif (closerT == 34.5):
        L = ["Mild", "Passion", "Balmy"]
    elif (closerT == 35):
        L = ["Warm", "Hope", "Toasty"]
    elif (closerT == 35.5):
        L = ["Warm", "Energetic", "Snug"]
    elif (closerT == 36):
        L = ["Hot", "Enchanted", "Blistering"]
    elif (closerT == 36.5):
        L = ["Hot", "Stressful", "Sizzling"]
    elif (closerT == 37):
        L + ["Very hot", "Sweltering", "Torrid"]
    elif (closerT == 37.5):
        L = ["Very hot", "Scorching", "Oppressive"]
    else :
        L = ["Extremely hot", "Suffocating", "Furnace-like"]
    
    return L

# Le premier mot de la liste
def premier_mot(T):

    return liste_mots_temp(T)[0]
