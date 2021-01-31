def getRandomExample(language, difficulty, window):
    """
    Function return random example from xml file
        :param language: Language in string (small letters)
        :param difficulty: Difficulty level (easy, medium, hard)
        :return: Random example
    """
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
    # End of getting random example
    # Start of getting typeable characters number of this example
    numberOfTypeableCharacters=0
    for i in range(0,len(result)):
        if result[i]!=" " or result[i]!="\t":
            numberOfTypeableCharacters+=1
    # Setting numberOfTypeableCharacters in array in amin window

    window.examplesLength[window.currentRound-1]=numberOfTypeableCharacters
    
    return result 


def checkSpelling(window, properText, userInputField):
    """
    checkSpelling check text of userInput with provided example
        :param properText: text from example
        :param difficulty: userInputField from main window
        :return: -1 when it's not norrect, 1 when round ended
    """
    from PyQt5.QtGui import QTextCursor

    text=userInputField.toPlainText()
    if len(text)<=len(properText) and len(text)>0:

        if text[-1]=="\t":
            tmptext=""
            for i in range(0,len(text)-1):
                tmptext+=text[i]
            tmptext+="    "
            userInputField.setPlainText(tmptext)

            cursor=userInputField.textCursor()
            cursor.setPosition(len(tmptext))
            userInputField.setTextCursor(cursor)
            return 0

        for i in range(0, len(userInputField.toPlainText())):
            if properText[i]!=text[i]:
                userInputField.setStyleSheet("background-color: #ff0000; border: 1px solid red; border-radius: 5px;")
                return -1
            else:
                userInputField.setStyleSheet("background-color: #596ed9; border: 1px solid #596ed9; border-radius: 5px;")
        if len(text)==len(properText):
            userInputField.setPlainText("")
            return 1


