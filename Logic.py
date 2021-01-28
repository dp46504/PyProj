"""
getRandomExample

zwraca tekst losowo wybranego przykladu (w string) o wyznaczonym jezyku i poziomie trudnosci.

wejscia:
    language - nazwa jezyka w stringu np. python (wszystko z malych)
    difficulty - poziom trudnosci w stringu (easy, medium, hard)

wyjscia:
    tekstowa reprezantacja jednego przykladu
"""
def getRandomExample(language, difficulty):
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
    tmp=root[lang][diff][rndChildIndex].text
    result=""
    
    for i in range(1,len(tmp)-1):
        result+=tmp[i]

    return result 



"""
checkSpelling

zwraca true jesli tekst pokrywa sie z przykladem

wejscia:
    properText - tekst przykladu (zwracany przez funkcje getRandomText)
    userInput - zawartosc pola input
    userInputField - userInput z glownego okna aby moc sie z nim laczyc

wyjscia:
    true kiedy tekst sie pokrywa.
    False w przeciwnym przypdaku.
    Zmienia border color inputa
"""
def checkSpelling(properText, userInputField):
    text=userInputField.text()
    if len(text)<=len(properText):
        for i in range(0, len(text)):
            if properText[i]!=text[i]:
                userInputField.setStyleSheet("background-color: #ff0000; border: 1px solid red; border-radius: 5px;")
                return 0
            else:
                userInputField.setStyleSheet("background-color: #596ed9; border: 1px solid #596ed9; border-radius: 5px;")
        print(len(text), len(properText))
        if len(text)==len(properText):
            print("DONE DONE DONE")
