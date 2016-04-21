import xlsxwriter

workbook = xlsxwriter.Workbook('ParsedData1.xlsx')
switchSheet = workbook.add_worksheet('Switch')
blocksSheet = workbook.add_worksheet('Blocks')
f = open('text.txt','r', encoding='utf-16-le')

#mata data for switch sheet
switchSheet.write(0, 0, 'switch')
switchSheet.write(0, 1, 'type')

switchSheet.write(0,4,'num')
switchSheet.write(0,5,'type')

switchSheet.write(1,4,'1')
switchSheet.write(1,5,'Neut - Neut')

switchSheet.write(2,4,'2')
switchSheet.write(2,5,'Neut - Emo')

switchSheet.write(3,4,'3')
switchSheet.write(3,5,'Emo - Emo')

switchSheet.write(4,4,'4')
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
row = 1
column =0
user = 0
block = 0
for line in lines[2:]:
    dataArr = line.split()
    if(len(dataArr) < 3): #ignore start block line
        continue
    if(dataArr[3] == '.'): #if it is dammie
        user = dataArr[0]
        row+=1
        continue

    if(dataArr[1] == '1'): #if it is first experiment
        if(dataArr[2] == 'Neut' and dataArr[3] == 'Neut'):
            switchSheet.write(row, 0, 0)
            switchSheet.write(row, 1, 1)
        elif(dataArr[2] == 'Neut' and dataArr[3] == 'Emo'):
            switchSheet.write(row, 0, 1)
            switchSheet.write(row, 1, 2)
        elif(dataArr[2] == 'Emo' and dataArr[3] == 'Emo'):
            switchSheet.write(row, 0, 0)
            switchSheet.write(row, 1, 3)
        elif(dataArr[2] == 'Emo' and dataArr[3] == 'Neut'):
            switchSheet.write(row, 0, 1)
            switchSheet.write(row, 1, 4)
        else:
            print("error!!!")
    else:
        if(dataArr[2] == dataArr[3]):
            switchSheet.write(row, 0, 0)
        else:
            switchSheet.write(row, 0, 1)

    row+=1
f.close()

workbook.close()