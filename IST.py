import xlsxwriter

workbook = xlsxwriter.Workbook('ParsedData.xlsx')
switchSheet = workbook.add_worksheet('Switch')
blocksSheet = workbook.add_worksheet('Blocks')

#mata data for switch sheet
switchSheet.write(0, 0, 'switch')
switchSheet.write(0, 1, 'type')

switchSheet.write(0,4,'num')
switchSheet.write(0,5,'type')

switchSheet.write(1,4,1)
switchSheet.write(1,5,'Neut - Neut')

switchSheet.write(2,4,2)
switchSheet.write(2,5,'Neut - Emo')

switchSheet.write(3,4,3)
switchSheet.write(3,5,'Emo - Emo')

switchSheet.write(4,4,4)
switchSheet.write(4,5,'Emo - Neut')

#mata data for blocks sheet
blocksSheet.write(0, 0, 'User number')
blocksSheet.write(0, 1, 'version')
blocksSheet.write(0, 2, 'block number')
blocksSheet.write(0, 3, 'Neut difference')
blocksSheet.write(0, 4, 'Emo difference')
blocksSheet.write(0, 5, 'Verb difference')
blocksSheet.write(0, 6, 'Noun difference')
blocksSheet.write(0, 7, 'Accuracy')

f = open('text.txt','r', encoding='utf-16-le')
lines = f.readlines()

#place of the relevant varibels
subjectPlace = -1
sessionPlace = -1
stimCatPlace = -1
lastCategoryPlace = -1
questionOneTypePlace = -1
questionTwoAnswerPlace = -1
questionOneAnswerPlace = -1

varNameLine = lines[1].split()

varNumber = 0
for var in varNameLine:
    if(var == 'Subject'):
        subjectPlace = varNumber
    elif(var == 'Session'):
        sessionPlace = varNumber
    elif(var == 'StimCat'):
        stimCatPlace = varNumber
    elif(var == 'LactCategory'): #the misspelling in origin
        lastCategoryPlace = varNumber
    elif(var == 'Q1SlidePath'):
        questionOneTypePlace = varNumber
    elif(var == 'Q2Slide.RESP'):
        questionTwoAnswerPlace = varNumber
    elif(var == 'Q1Slide.RESP'):
        questionOneAnswerPlace = varNumber
    varNumber+=1

lastline = []

#block sheet variables:
user = -1
block = 1
NeutCount = 0
EmoCount = 0
VerbCount = 0
NounCount = 0
blockSheetRow = 1

def resetWords():
    global NeutCount
    global EmoCount
    global VerbCount
    global NounCount
    NeutCount=0
    EmoCount = 0
    VerbCount = 0
    NounCount = 0

def addWord(word):
    global NeutCount
    global EmoCount
    global VerbCount
    global NounCount
    if(word == 'Neut'):
        NeutCount+=1
    elif(word == 'Emo'):
        EmoCount+=1
    elif(word == 'Verb'):
        VerbCount+=1
    elif(word == 'Noun'):
        NounCount+=1
    else:
        print("unknown - " + word)


switchSheetRow = 1

for line in lines[2:]:
    dataArr = line.split()
    if(len(dataArr) < 3): #ignore start block line
        continue
    if(dataArr[lastCategoryPlace] == '.'): #if it is dammie
        if(len(lastline) > 1) : #if it's not the first blcok
            if((int)(user) == (int)(lastline[subjectPlace])):
                block += 1
            else:
                user = (int)(lastline[subjectPlace])
                block = 1
            blocksSheet.write(blockSheetRow, 0, user)
            blocksSheet.write(blockSheetRow, 1, (int)(lastline[1]))
            blocksSheet.write(blockSheetRow, 2,block)
            if(lastline[sessionPlace]=="1"): #Emo/Neut
                if(lastline[questionOneTypePlace] == 'Stimuli/Instructions/Slide1.png'): #first question is abuot emo
                    EmoDif = abs(EmoCount - (int)(lastline[questionOneAnswerPlace].split('{')[0]))
                    NeutDif = abs(NeutCount - (int)(lastline[questionTwoAnswerPlace].split('{')[0]))
                else:
                    EmoDif = abs(EmoCount - (int)(lastline[questionTwoAnswerPlace].split('{')[0]))
                    NeutDif = abs(NeutCount - (int)(lastline[questionOneAnswerPlace].split('{')[0]))
                blocksSheet.write(blockSheetRow, 3,EmoDif)
                blocksSheet.write(blockSheetRow, 4,NeutDif)
                if(EmoDif == 0 and NeutDif == 0):
                    blocksSheet.write(blockSheetRow, 7,1)
                else:
                    blocksSheet.write(blockSheetRow, 7,0)

            else:  #Verb/Noun
                if(lastline[questionOneTypePlace] == 'Stimuli/Instructions/Slide3.png'): #first question is about verb
                    verbDif = abs(VerbCount - (int)(lastline[questionOneAnswerPlace].split('{')[0]))
                    NounDif = abs(NounCount - (int)(lastline[questionTwoAnswerPlace].split('{')[0]))
                else:
                    verbDif = abs(VerbCount - (int)(lastline[questionTwoAnswerPlace].split('{')[0]))
                    NounDif = abs(NounCount - (int)(lastline[questionOneAnswerPlace].split('{')[0]))
                blocksSheet.write(blockSheetRow, 5,verbDif)
                blocksSheet.write(blockSheetRow, 6,NounDif)
                if(verbDif == 0 and NounDif == 0):
                    blocksSheet.write(blockSheetRow, 7,1)
                else:
                    blocksSheet.write(blockSheetRow, 7,0)

            blockSheetRow+=1
            resetWords()


        addWord(dataArr[stimCatPlace])
        switchSheetRow+=1
        continue

    #from here - handle step
    addWord(dataArr[stimCatPlace])

    if(dataArr[sessionPlace] == '1'): #if it is first experiment
        if(dataArr[stimCatPlace] == 'Neut' and dataArr[lastCategoryPlace] == 'Neut'):
            switchSheet.write(switchSheetRow, 0, 0)
            switchSheet.write(switchSheetRow, 1, 1)
        elif(dataArr[stimCatPlace] == 'Neut' and dataArr[lastCategoryPlace] == 'Emo'):
            switchSheet.write(switchSheetRow, 0, 1)
            switchSheet.write(switchSheetRow, 1, 2)
        elif(dataArr[stimCatPlace] == 'Emo' and dataArr[lastCategoryPlace] == 'Emo'):
            switchSheet.write(switchSheetRow, 0, 0)
            switchSheet.write(switchSheetRow, 1, 3)
        elif(dataArr[stimCatPlace] == 'Emo' and dataArr[lastCategoryPlace] == 'Neut'):
            switchSheet.write(switchSheetRow, 0, 1)
            switchSheet.write(switchSheetRow, 1, 4)
        else:
            print("error!!!")
    else:
        if(dataArr[stimCatPlace] == dataArr[lastCategoryPlace]):
            switchSheet.write(switchSheetRow, 0, 0)
        else:
            switchSheet.write(switchSheetRow, 0, 1)
    lastline = dataArr
    switchSheetRow+=1
f.close()

workbook.close()