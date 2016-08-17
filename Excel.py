import xlsxwriter
import datetime

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

        self.metaSheet = self.workbook.add_worksheet('Meta data')
        self.trailsSheet = self.workbook.add_worksheet('Trails')
        self.blocksSheet = self.workbook.add_worksheet('Blocks')
        self.usersSheet = self.workbook.add_worksheet('Users')

        #add titles for all the sheets
        self.metaSheetTitles()
        self.trailsSheetTitles()
        self.blocksSheetTitles()
        self.usersSheetTitles()

    def printUser(self,user):
        self.usersSheet.write(self.timingSheetRow, 0, user.id)
        self.usersSheet.write(self.timingSheetRow, 1, user.neutral_S.getMean())
        self.usersSheet.write(self.timingSheetRow, 2, user.neutral_NS.getMean())
        self.usersSheet.write(self.timingSheetRow, 3, user.neutral_S - user.neutral_NS)
        self.usersSheet.write(self.timingSheetRow, 4, user.emotional_NN.getMean(1))
        self.usersSheet.write(self.timingSheetRow, 5, user.emotional_NE.getMean(1))
        self.usersSheet.write(self.timingSheetRow, 6, user.emotional_EN.getMean(1))
        self.usersSheet.write(self.timingSheetRow, 7, user.emotional_EE.getMean(1))
        self.usersSheet.write(self.timingSheetRow, 8, user.emotional_S.getMean())
        self.usersSheet.write(self.timingSheetRow, 9, user.emotional_NS.getMean())
        self.usersSheet.write(self.timingSheetRow, 10, user.emotional_S - user.emotional_NS)
        self.usersSheet.write(self.timingSheetRow, 11, user.mean)
        self.usersSheet.write(self.timingSheetRow, 12, user.standardDeviation)
        self.timingSheetRow += 1

        for block in user.blocks:
            if(len(block.trials) == 0):
                continue
            self.printBlock(block)

    def printBlock(self,block):
        self.blocksSheet.write(self.blockSheetRow, 0, block.userId)
        self.blocksSheet.write(self.blockSheetRow, 1, block.type)
        self.blocksSheet.write(self.blockSheetRow, 2, block.id)
        if(block.type == '1'):
            if(block.trials[0].firstQuestionSlide == '1'):
                emoDiff = abs(block.emoCount -  block.trials[0].firstQuestionAnswer)
                neutDiff = abs(block.neutCount - block.trials[0].secondQuestionAnswer)
            else:
                emoDiff = abs(block.emoCount -  block.trials[0].secondQuestionAnswer)
                neutDiff = abs(block.neutCount - block.trials[0].firstQuestionAnswer)
            self.blocksSheet.write(self.blockSheetRow, 3,emoDiff)
            self.blocksSheet.write(self.blockSheetRow, 4,neutDiff)
            if(emoDiff == 0 and neutDiff == 0):
                self.blocksSheet.write(self.blockSheetRow, 7,1)
            else:
                self.blocksSheet.write(self.blockSheetRow, 7,0)
        else:
            if(block.trials[0].firstQuestionSlide == '3'):
                verbDiff = abs(block.verbCount -  block.trials[0].firstQuestionAnswer)
                nounDiff = abs(block.nounCount - block.trials[0].secondQuestionAnswer)
            else:
                verbDiff = abs(block.verbCount -  block.trials[0].secondQuestionAnswer)
                nounDiff = abs(block.nounCount - block.trials[0].firstQuestionAnswer)
            self.blocksSheet.write(self.blockSheetRow, 5,verbDiff)
            self.blocksSheet.write(self.blockSheetRow, 6,nounDiff)
            if(verbDiff == 0 and nounDiff == 0):
                self.blocksSheet.write(self.blockSheetRow, 7,1)
            else:
                self.blocksSheet.write(self.blockSheetRow, 7,0)
        self.blockSheetRow += 1

        for trial in block.trials:
            self.printTrail(trial)

    def printTrail(self,trial):
        self.trailsSheet.write(self.switchSheetRow, 0, trial.userId)
        self.trailsSheet.write(self.switchSheetRow, 1, trial.timing)
        if(trial.isDummy()):
            self.switchSheetRow += 1
            return

        if(trial.isSwitch()):
            self.trailsSheet.write(self.switchSheetRow, 2, 1)
        else:
             self.trailsSheet.write(self.switchSheetRow, 2, 0)
        if(trial.type == '1'):
            if(trial.category == 'Neut'):
                if(trial.lastCategory == 'Neut'):
                    self.trailsSheet.write(self.switchSheetRow, 3, 1)
                else:
                    self.trailsSheet.write(self.switchSheetRow, 3, 2)
            else:
                if(trial.lastCategory == 'Neut'):
                    self.trailsSheet.write(self.switchSheetRow, 3, 4)
                else:
                    self.trailsSheet.write(self.switchSheetRow, 3, 3)

        self.trailsSheet.write(self.switchSheetRow, 4, trial.standardScore)

        self.switchSheetRow += 1


    def metaSheetTitles(self):
        self.metaSheet.write(0,0, 'created at')
        self.metaSheet.write(0,1, datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))

        self.metaSheet.merge_range('G1:H1', 'trail switch index', self.merge_format)
        self.metaSheet.write(1, 6, 'num')
        self.metaSheet.write(1, 7, 'type')

        self.metaSheet.write(2, 6, 1)
        self.metaSheet.write(2, 7, 'Neut - Neut')

        self.metaSheet.write(3, 6, 2)
        self.metaSheet.write(3, 7, 'Neut - Emo')

        self.metaSheet.write(4, 6, 3)
        self.metaSheet.write(4, 7, 'Emo - Emo')

        self.metaSheet.write(5, 6, 4)
        self.metaSheet.write(5, 7, 'Emo - Neut')

    def trailsSheetTitles(self):
        self.trailsSheet.write(0, 0, 'User id')
        self.trailsSheet.write(0, 1, 'RT')
        self.trailsSheet.write(0, 2, 'Switch')
        self.trailsSheet.write(0, 3, 'Type')
        self.trailsSheet.write(0, 4, 'standard deviations')

    def blocksSheetTitles(self):
        self.blocksSheet.write(0, 0, 'User number')
        self.blocksSheet.write(0, 1, 'version')
        self.blocksSheet.write(0, 2, 'block number')
        self.blocksSheet.write(0, 3, 'Neut difference')
        self.blocksSheet.write(0, 4, 'Emo difference')
        self.blocksSheet.write(0, 5, 'Verb difference')
        self.blocksSheet.write(0, 6, 'Noun difference')
        self.blocksSheet.write(0, 7, 'Accuracy')

    def usersSheetTitles(self):
        self.usersSheet.merge_range('B1:D1', 'Neutral version', self.merge_format)
        self.usersSheet.merge_range('E1:K1', 'Emotional version', self.merge_format)

        self.usersSheet.write(1, 0, 'subject id')
        self.usersSheet.write(1, 1, 'S - Neutral')
        self.usersSheet.write(1, 2, 'NS - Neutral')
        self.usersSheet.write(1, 3, 'ISC - Neutral')
        self.usersSheet.write(1, 4, 'N-N - Emotinal')
        self.usersSheet.write(1, 5, 'N-E - Emotinal')
        self.usersSheet.write(1, 6, 'E-N - Emotinal')
        self.usersSheet.write(1, 7, 'E-E - Emotinal')
        self.usersSheet.write(1, 8, 'S - Emotinal')
        self.usersSheet.write(1, 9, 'NS - Emotinal')
        self.usersSheet.write(1, 10, 'ISC - Emotinal')

        self.usersSheet.write(1, 11, 'Mean')
        self.usersSheet.write(1, 12, 'Standard deviation')

    def close(self):
        self.workbook.close()