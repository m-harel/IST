import xlsxwriter

workbook = xlsxwriter.Workbook('ParsedData.xlsx')
switchSheet = workbook.add_worksheet('Switch')
blocksSheet = workbook.add_worksheet('Blocks')
f = open('text.txt','r', encoding='utf-16-le')

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

lines = f.readlines()
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
    if(dataArr[3] == '.'): #if it is dammie
        if(len(lastline) > 1) : #if it's not the first blcok
            if((int)(user) == (int)(lastline[0])):
                block += 1
            else:
                user = (int)(lastline[0])
                block = 1
            blocksSheet.write(blockSheetRow, 0, user)
            blocksSheet.write(blockSheetRow, 1, (int)(lastline[1]))
            blocksSheet.write(blockSheetRow, 2,block)
            if(lastline[1]=="1"): #Emo/Neut
                if(lastline[6] == 'Stimuli/Instructions/Slide1.png'): #first question is abuot emo
                    EmoDif = abs(EmoCount - (int)(lastline[8].split('{')[0]))
                    NeutDif = abs(NeutCount - (int)(lastline[7].split('{')[0]))
                else:
                    EmoDif = abs(EmoCount - (int)(lastline[7].split('{')[0]))
                    NeutDif = abs(NeutCount - (int)(lastline[8].split('{')[0]))
                blocksSheet.write(blockSheetRow, 3,EmoDif)
                blocksSheet.write(blockSheetRow, 4,NeutDif)
                if(EmoDif == 0 and NeutDif == 0):
                    blocksSheet.write(blockSheetRow, 7,1)
                else:
                    blocksSheet.write(blockSheetRow, 7,0)

            else:  #Verb/Noun
                if(lastline[6] == 'Stimuli/Instructions/Slide3.png'): #first question is about verb
                    verbDif = abs(VerbCount - (int)(lastline[8].split('{')[0]))
                    NounDif = abs(NounCount - (int)(lastline[7].split('{')[0]))
                else:
                    verbDif = abs(VerbCount - (int)(lastline[7].split('{')[0]))
                    NounDif = abs(NounCount - (int)(lastline[8].split('{')[0]))
                blocksSheet.write(blockSheetRow, 5,verbDif)
                blocksSheet.write(blockSheetRow, 6,NounDif)
                if(verbDif == 0 and NounDif == 0):
                    blocksSheet.write(blockSheetRow, 7,1)
                else:
                    blocksSheet.write(blockSheetRow, 7,0)

            blockSheetRow+=1
            resetWords()


        addWord(dataArr[2])
        switchSheetRow+=1
        continue

    addWord(dataArr[2])
    if(dataArr[1] == '1'): #if it is first experiment
        if(dataArr[2] == 'Neut' and dataArr[3] == 'Neut'):
            switchSheet.write(switchSheetRow, 0, 0)
            switchSheet.write(switchSheetRow, 1, 1)
        elif(dataArr[2] == 'Neut' and dataArr[3] == 'Emo'):
            switchSheet.write(switchSheetRow, 0, 1)
            switchSheet.write(switchSheetRow, 1, 2)
        elif(dataArr[2] == 'Emo' and dataArr[3] == 'Emo'):
            switchSheet.write(switchSheetRow, 0, 0)
            switchSheet.write(switchSheetRow, 1, 3)
        elif(dataArr[2] == 'Emo' and dataArr[3] == 'Neut'):
            switchSheet.write(switchSheetRow, 0, 1)
            switchSheet.write(switchSheetRow, 1, 4)
        else:
            print("error!!!")
    else:
        if(dataArr[2] == dataArr[3]):
            switchSheet.write(switchSheetRow, 0, 0)
        else:
            switchSheet.write(switchSheetRow, 0, 1)
    lastline = dataArr
    switchSheetRow+=1
f.close()

workbook.close()