import xlsxwriter

class Excel:
    timingSheetRow = 2
    blockSheetRow = 1
    switchSheetRow = 1

    def __init__(self,fileName):
        self.workbook = xlsxwriter.Workbook(fileName)
        self.merge_format = self.workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'})

        self.switchSheet = self.workbook.add_worksheet('Switch')
        self.blocksSheet = self.workbook.add_worksheet('Blocks')
        self.timingSheet = self.workbook.add_worksheet('Timing')

        #add titles for all the sheets
        self.SwitchSheetTitles()
        self.blocksSheetTitles()
        self.timingSheetTitles()

    def printUser(self,user):
        self.timingSheet.write(self.timingSheetRow,0, user.id)
        self.timingSheet.write(self.timingSheetRow,1, user.neutral_S.getMean())
        self.timingSheet.write(self.timingSheetRow,2, user.neutral_NS.getMean())
        self.timingSheet.write(self.timingSheetRow,3, user.neutral_S - user.neutral_NS)
        self.timingSheet.write(self.timingSheetRow,4, user.emotional_NN.getMean(1))
        self.timingSheet.write(self.timingSheetRow,5, user.emotional_NE.getMean(1))
        self.timingSheet.write(self.timingSheetRow,6, user.emotional_EN.getMean(1))
        self.timingSheet.write(self.timingSheetRow,7, user.emotional_EE.getMean(1))
        self.timingSheet.write(self.timingSheetRow,8, user.emotional_S.getMean())
        self.timingSheet.write(self.timingSheetRow,9, user.emotional_NS.getMean())
        self.timingSheet.write(self.timingSheetRow,10, user.emotional_S - user.emotional_NS)
        self.timingSheetRow += 1

        for block in user.blocks:
            if(len(block.questions) == 0):
                continue
            self.printBlock(block)

    def printBlock(self,block):
        self.blocksSheet.write(self.blockSheetRow, 0, block.userId)
        self.blocksSheet.write(self.blockSheetRow, 1, block.type)
        self.blocksSheet.write(self.blockSheetRow, 2, block.id)
        if(block.type == '1'):
            if(block.questions[0].firstQuestionSlide == '1'):
                emoDiff = abs(block.emoCount -  block.questions[0].firstQuestionAnswer)
                neutDiff = abs(block.neutCount - block.questions[0].secondQuestionAnswer)
            else:
                emoDiff = abs(block.emoCount -  block.questions[0].secondQuestionAnswer)
                neutDiff = abs(block.neutCount - block.questions[0].firstQuestionAnswer)
            self.blocksSheet.write(self.blockSheetRow, 3,emoDiff)
            self.blocksSheet.write(self.blockSheetRow, 4,neutDiff)
            if(emoDiff == 0 and neutDiff == 0):
                self.blocksSheet.write(self.blockSheetRow, 7,1)
            else:
                self.blocksSheet.write(self.blockSheetRow, 7,0)
        else:
            if(block.questions[0].firstQuestionSlide == '3'):
                verbDiff = abs(block.verbCount -  block.questions[0].firstQuestionAnswer)
                nounDiff = abs(block.nounCount - block.questions[0].secondQuestionAnswer)
            else:
                verbDiff = abs(block.verbCount -  block.questions[0].secondQuestionAnswer)
                nounDiff = abs(block.nounCount - block.questions[0].firstQuestionAnswer)
            self.blocksSheet.write(self.blockSheetRow, 5,verbDiff)
            self.blocksSheet.write(self.blockSheetRow, 6,nounDiff)
            if(verbDiff == 0 and nounDiff == 0):
                self.blocksSheet.write(self.blockSheetRow, 7,1)
            else:
                self.blocksSheet.write(self.blockSheetRow, 7,0)
        self.blockSheetRow += 1

        for question in block.questions:
            self.printQuestion(question)

    def printQuestion(self,question):
        if(question.isDummy()):
            self.switchSheetRow += 1
            return
        if(question.isSwitch()):
            self.switchSheet.write(self.switchSheetRow, 0, 0)
        else:
             self.switchSheet.write(self.switchSheetRow, 0, 1)
        if(question.type == '1'):
            if(question.category == 'Neut'):
                if(question.lastCategory == 'Neut'):
                    self.switchSheet.write(self.switchSheetRow, 1, 1)
                else:
                    self.switchSheet.write(self.switchSheetRow, 1, 2)
            else:
                if(question.lastCategory == 'Neut'):
                    self.switchSheet.write(self.switchSheetRow, 1, 4)
                else:
                    self.switchSheet.write(self.switchSheetRow, 1, 3)
        self.switchSheetRow += 1

    def SwitchSheetTitles(self):
        self.switchSheet.write(0, 0, 'switch')
        self.switchSheet.write(0, 1, 'type')

        self.switchSheet.write(0,4,'num')
        self.switchSheet.write(0,5,'type')

        self.switchSheet.write(1,4,1)
        self.switchSheet.write(1,5,'Neut - Neut')

        self.switchSheet.write(2,4,2)
        self.switchSheet.write(2,5,'Neut - Emo')

        self.switchSheet.write(3,4,3)
        self.switchSheet.write(3,5,'Emo - Emo')

        self.switchSheet.write(4,4,4)
        self.switchSheet.write(4,5,'Emo - Neut')

    def blocksSheetTitles(self):
        self.blocksSheet.write(0, 0, 'User number')
        self.blocksSheet.write(0, 1, 'version')
        self.blocksSheet.write(0, 2, 'block number')
        self.blocksSheet.write(0, 3, 'Neut difference')
        self.blocksSheet.write(0, 4, 'Emo difference')
        self.blocksSheet.write(0, 5, 'Verb difference')
        self.blocksSheet.write(0, 6, 'Noun difference')
        self.blocksSheet.write(0, 7, 'Accuracy')

    def timingSheetTitles(self):
        self.timingSheet.merge_range('B1:D1', 'Neutral version', self.merge_format)
        self.timingSheet.merge_range('E1:K1', 'Emotional version', self.merge_format)

        self.timingSheet.write(1,0, 'subject id')
        self.timingSheet.write(1,1, 'S')
        self.timingSheet.write(1,2, 'NS')
        self.timingSheet.write(1,3, 'ISC')
        self.timingSheet.write(1,4, 'N-N')
        self.timingSheet.write(1,5, 'N-E')
        self.timingSheet.write(1,6, 'E-N')
        self.timingSheet.write(1,7, 'E-E')
        self.timingSheet.write(1,8, 'S')
        self.timingSheet.write(1,9, 'NS')
        self.timingSheet.write(1,10, 'ISC')

    def close(self):
        self.workbook.close()