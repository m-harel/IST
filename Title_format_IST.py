
def SwitchSheetTitles(workSheet):
    workSheet.write(0, 0, 'switch')
    workSheet.write(0, 1, 'type')

    workSheet.write(0,4,'num')
    workSheet.write(0,5,'type')

    workSheet.write(1,4,1)
    workSheet.write(1,5,'Neut - Neut')

    workSheet.write(2,4,2)
    workSheet.write(2,5,'Neut - Emo')

    workSheet.write(3,4,3)
    workSheet.write(3,5,'Emo - Emo')

    workSheet.write(4,4,4)
    workSheet.write(4,5,'Emo - Neut')

def blocksSheetTitles(workSheet):
    workSheet.write(0, 0, 'User number')
    workSheet.write(0, 1, 'version')
    workSheet.write(0, 2, 'block number')
    workSheet.write(0, 3, 'Neut difference')
    workSheet.write(0, 4, 'Emo difference')
    workSheet.write(0, 5, 'Verb difference')
    workSheet.write(0, 6, 'Noun difference')
    workSheet.write(0, 7, 'Accuracy')

def timingSheetTitles(workSheet, format):
    workSheet.merge_range('B1:D1', 'Neutral version', format)
    workSheet.merge_range('E1:K1', 'Emotional version', format)

    workSheet.write(1,0, 'subject id')
    workSheet.write(1,1, 'S')
    workSheet.write(1,2, 'NS')
    workSheet.write(1,3, 'ISC')
    workSheet.write(1,4, 'N-N')
    workSheet.write(1,5, 'N-E')
    workSheet.write(1,6, 'E-N')
    workSheet.write(1,7, 'E-E')
    workSheet.write(1,8, 'S')
    workSheet.write(1,9, 'NS')
    workSheet.write(1,10, 'ISC')