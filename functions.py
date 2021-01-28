"""
getRandomText

zwraca tekst losowo wybranego przykladu (w string) o wyznaczonym jezyku i poziomie trudnosci.

wejscia:
    language - nazwa jezyka w stringu np. python (wszystko z malych)
    difficulty - poziom trudnosci w stringu (easy, medium, hard)

wyjscia:
    tekstowa reprezantacja jednego przykladu
"""
def getRandomText(language, difficulty):
    import xml.etree.ElementTree as ET
    import random
    path="texts\\"+language+".xml"
    tree=ET.parse(path)
    root=tree.getroot()
    lang=0
    diff=0
    if language =="python":
        lang=0
    elif language =="cpp":
        lang=1

    if difficulty == "easy":
        diff=0
    elif difficulty == "medium":
        diff=1
    elif difficulty == "hard":
        diff=2

    numOfChildren=len(root[lang][diff])-1
    rndChildIndex=random.randint(0, numOfChildren)
    
    return root[lang][diff][rndChildIndex].text



"""
checkSpelling

zwraca true jesli tekst pokrywa sie z przykladem

wejscia:
    properText - tekst przykladu (zwracany przez funkcje getRandomText)
    userInput - zawartosc pola input

wyjscia:
    true kiedy tekst sie pokrywa.
    False w przeciwnym przypdaku.
"""
# def checkSpelling(properText, userInput, ):

    