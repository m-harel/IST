import xlsxwriter
import Title_format_IST
import Mean

workbook = xlsxwriter.Workbook('ParsedData.xlsx')
merge_format = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter'})

switchSheet = workbook.add_worksheet('Switch')
blocksSheet = workbook.add_worksheet('Blocks')
timingSheet = workbook.add_worksheet('Timing')



#add titles for all the sheets
Title_format_IST.SwitchSheetTitles(switchSheet)
Title_format_IST.blocksSheetTitles(blocksSheet)
Title_format_IST.timingSheetTitles(timingSheet,merge_format)


f = open('text.txt','r', encoding='utf-16-le')
lines = f.readlines()

#place of the relevant varibels
subjectPlace = -1
sessionPlace = -1
stimCatPlace = -1
lastCategoryPlace = -1
timingPlace = -1
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
    elif(var == 'StimTextDisp.RT'):
        timingPlace = varNumber
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

#timing sheet variables:
neutral_S = Mean.Mean()
neutral_NS = Mean.Mean()
emotional_NN = Mean.Mean()
emotional_NE = Mean.Mean()
emotional_EN = Mean.Mean()
emotional_EE = Mean.Mean()
emotional_S = Mean.Mean()
emotional_NS = Mean.Mean()
current_user = -1
timingSheetRow = 2

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
    if(len(dataArr) < 3): #start of a block. here we can find the user id replace
        if((int)(user) is not current_user): #if user ended
            if(current_user is not -1): #if it's not the first user
                timingSheet.write(timingSheetRow,0, current_user)
                timingSheet.write(timingSheetRow,1, neutral_S.getMean())
                timingSheet.write(timingSheetRow,2, neutral_NS.getMean())
                timingSheet.write(timingSheetRow,3, neutral_S.getMean(1) - neutral_NS.getMean(1))
                timingSheet.write(timingSheetRow,4, emotional_NN.getMean(1))
                timingSheet.write(timingSheetRow,5, emotional_NE.getMean(1))
                timingSheet.write(timingSheetRow,6, emotional_EN.getMean(1))
                timingSheet.write(timingSheetRow,7, emotional_EE.getMean(1))
                timingSheet.write(timingSheetRow,8, emotional_S.getMean())
                timingSheet.write(timingSheetRow,9, emotional_NS.getMean())
                timingSheet.write(timingSheetRow,10, emotional_S.getMean(1) - emotional_NS.getMean(1))
                timingSheetRow += 1
            current_user = (int)(user)
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
            emotional_NN.add((int)(dataArr[timingPlace]))
            emotional_NS.add((int)(dataArr[timingPlace]))
        elif(dataArr[stimCatPlace] == 'Neut' and dataArr[lastCategoryPlace] == 'Emo'):
            switchSheet.write(switchSheetRow, 0, 1)
            switchSheet.write(switchSheetRow, 1, 2)
            emotional_NE.add((int)(dataArr[timingPlace]))
            emotional_S.add((int)(dataArr[timingPlace]))
        elif(dataArr[stimCatPlace] == 'Emo' and dataArr[lastCategoryPlace] == 'Emo'):
            switchSheet.write(switchSheetRow, 0, 0)
            switchSheet.write(switchSheetRow, 1, 3)
            emotional_EE.add((int)(dataArr[timingPlace]))
            emotional_NS.add((int)(dataArr[timingPlace]))
        elif(dataArr[stimCatPlace] == 'Emo' and dataArr[lastCategoryPlace] == 'Neut'):
            switchSheet.write(switchSheetRow, 0, 1)
            switchSheet.write(switchSheetRow, 1, 4)
            emotional_EN.add((int)(dataArr[timingPlace]))
            emotional_S.add((int)(dataArr[timingPlace]))
        else:
            print("error!!!")
    else:
        if(dataArr[stimCatPlace] == dataArr[lastCategoryPlace]):
            switchSheet.write(switchSheetRow, 0, 0)
            neutral_NS.add((int)(dataArr[timingPlace]))
        else:
            switchSheet.write(switchSheetRow, 0, 1)
            neutral_S.add((int)(dataArr[timingPlace]))
    lastline = dataArr
    switchSheetRow+=1
f.close()

workbook.close()