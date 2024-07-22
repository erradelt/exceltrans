Hier kommt noch Text

Nachdem die Excelliste eingelesen wurde, werden die einzelnen Zeilen der Liste per Regular Expression (RE) ausgelesen um Typ 
und Abmessungen des jeweiligen Bauteils zu bestimmen. Die einzelnen Teile der RE sind dabei wie folgt codiert

Index   Bedeutung
0       Art
1       Material
2       Breite
3       Tiefe
4       Hoehe
5       Front
6       Option_1
7       Option_2
8       Option_3

Index 0 - Art:
RG  ==  Regal
SHS ==  Sicherheitsschrank
HL  ==  Hakenleiste
TP  ==  Arbeitsplatte
HS  ==  Hochschrank
HA  ==  Hospitalausgaus
US  ==  Unterschrank
WS  ==  Wandschrank
ST  ==  Schreibtisch
RC  ==  Rollcontainer
MA  ==  Medienampel

Index 1 - Material:
HK  ==  Holzkunststoff
SBL ==  Stahlblech (Edelstahl)

Index 2 - Breite:
Breite Bauteil in cm

Index 3 - Tiefe:
Tiefe Bauteil in cm

Index 4 - Hoehe:
Hoehe Bauteil in cm

Index 5 - Front:
AU  ==  Abwurfunterschrank?
OO  ==  ???
FL  ==  ???
KB  ==  ???

Index 6 - Def. Front:
XX  ==  ohne Front
xT  ==  Tuer(en), x ist Anzahl der Tueren
Sx  ==  Schublade, x ist Anzahl Schubladen

Index 7 - Option_1:
X   ==  ohne
K   ==  ???
H   ==  ???
G   ==  ???
T   ==  Tablarauszug?

Index 8 - Option_2:
XXX ==  ohne 
xEB ==  Einlegeboden, x ist Anzahl Einlegeboden
ISO ==  Ausstattung mit ISO-Modul System
xME ==  Muelleimer, x ist Anzahl Muelleimer

Index 9 - Option_3: