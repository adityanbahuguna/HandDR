import tensorflow as tf
import matplotlib.pyplot as plt

# Variablen
# Keine Datentypen angeben!
zahl = 1
fliesskomma = 1.5
wort = "Hallo"
logik = True

# Bedingungen
if logik is True and 1 > 0:
    print("Yes")
elif logik is False:
    print("No")
else:
    print("n/a")

# Schleifen
for i in range(0, 10):
    print(i) # 0, 1,2,3,4,5,6,7,8,9
for i in range(10):
    print(i) # 0, 1,2,3,4,5,6,7,8,9
for i in range(2,12,3): #start,end+1,step
    print(i) #2, 5, 8, 11

# Listen
liste1 = [] # Leere Liste
liste2 = [1, 2, 3, 4] # Liste mit 4 Integer Zahlen
liste3 = [i for i in range(5)] # Liste mit: 0,1,2,3,4

for val in liste3:
    print(val) # 0,1,2,3,4

# Dictionarys
# Haben Key: Value Daten
dict1 = {} # Leeres Dict
dict2= {0: 'Jan', 1:'Franneck'} # Die Keys müssen keine Zahlen sein!
dict3 = {'Haus1': ['Zimmer', 'Bad', 'Küche', '60qm'], 'Haus2': ['Bad', 'Küche', 'Wohnzimmer', '76qm']}

for key, val in dict3.items():
    print(key, val) # Printet keys, vals aus
for key in dict3.keys():
    print(key) # Printet keys aus
for val in dict3.values():
    print(val) # Printet vals aus

for val in dict3.values():
    for v in val:
        print(v) # Gibt für Jedes Haus die einzelnen Werte aus

# Funktionen 
def multiply(n1, n2):
    result = n1 * n2
    return result

print( multiply(2,3) ) # 2 * 3 = 6

# Matplotlib kurze Einführung
import random

plt.xlabel('x-Werte')
plt.ylabel('y-Werte')
plt.plot([random.randint(1, (i+1) * 10) for i in range(100)])
plt.show()