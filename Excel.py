import xlsxwriter

class Excel:
    timingSheetRow = 2
    blockSheetRow = 1
    switchSheetRow = 1

    #column numbers in switch sheet - const
    SWITCH_SWITCH = 0
    SWITCH_TYPE = 1

    #column numbers in block sheet - const
    BLOCKS_USER_NUMBER = 0
    BLOCKS_VERSION = 1
    BLOCKS_BLOCK_NUMBER = 2
    BLOCKS_NEUT_DIFFERENCE = 3
    BLOCKS_EMO_DIFFERENCE = 4
    BLOCKS_VERB_DIFFERENCE = 5
    BLOCKS_NOUN_DIFFERENCE = 6
    BLOCKS_ACCURACY = 7

    #column numbers in timimng sheet - const
    TIMIMNG_SUBJECT_ID = 0
    TIMING_S_NEUTRAL = 1
    TIMING_NS_NEUTRAL = 2
    TIMING_ISC_NEUTRAL = 3
    TIMING_N_N_EMOTINAL = 4
    TIMING_N_E_EMOTINAL = 5
    TIMING_E_N_EMOTINAL = 6
    TIMIMNG_E_E_EMOTINAL = 7
    TIMIMNG_S_EMOTINAL = 8
    TIMIMNG_NS_EMOTINAL = 9
    TIMING_ISC_EMOTINAL = 10

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
        self.timingSheet.write(self.timingSheetRow,Excel.TIMIMNG_SUBJECT_ID, user.id)
        self.timingSheet.write(self.timingSheetRow,Excel.TIMING_S_NEUTRAL, user.neutral_S.getMean())
        self.timingSheet.write(self.timingSheetRow,Excel.TIMING_NS_NEUTRAL, user.neutral_NS.getMean())
        self.timingSheet.write(self.timingSheetRow,Excel.TIMING_ISC_NEUTRAL, user.neutral_S - user.neutral_NS)
        self.timingSheet.write(self.timingSheetRow,Excel.TIMING_N_N_EMOTINAL, user.emotional_NN.getMean(1))
        self.timingSheet.write(self.timingSheetRow,Excel.TIMING_N_E_EMOTINAL, user.emotional_NE.getMean(1))
        self.timingSheet.write(self.timingSheetRow,Excel.TIMING_E_N_EMOTINAL, user.emotional_EN.getMean(1))
        self.timingSheet.write(self.timingSheetRow,Excel.TIMIMNG_E_E_EMOTINAL, user.emotional_EE.getMean(1))
        self.timingSheet.write(self.timingSheetRow,Excel.TIMIMNG_S_EMOTINAL, user.emotional_S.getMean())
        self.timingSheet.write(self.timingSheetRow,Excel.TIMIMNG_NS_EMOTINAL, user.emotional_NS.getMean())
        self.timingSheet.write(self.timingSheetRow,Excel.TIMING_ISC_EMOTINAL, user.emotional_S - user.emotional_NS)
        self.timingSheetRow += 1

        for block in user.blocks:
            if(len(block.trials) == 0):
                continue
            self.printBlock(block)

    def printBlock(self,block):
        self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_USER_NUMBER, block.userId)
        self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_VERSION, block.type)
        self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_BLOCK_NUMBER, block.id)
        if(block.type == '1'):
            if(block.trials[0].firstQuestionSlide == '1'):
                emoDiff = abs(block.emoCount -  block.trials[0].firstQuestionAnswer)
                neutDiff = abs(block.neutCount - block.trials[0].secondQuestionAnswer)
            else:
                emoDiff = abs(block.emoCount -  block.trials[0].secondQuestionAnswer)
                neutDiff = abs(block.neutCount - block.trials[0].firstQuestionAnswer)
            self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_EMO_DIFFERENCE,emoDiff)
            self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_NEUT_DIFFERENCE,neutDiff)
            if(emoDiff == 0 and neutDiff == 0):
                self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_ACCURACY,1)
            else:
                self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_ACCURACY,0)
        else:
            if(block.trials[0].firstQuestionSlide == '3'):
                #print("a")
                #print(str(block.verbCount) + " " + str(block.trials[0].firstQuestionAnswer))
                #print(str(block.nounCount) + " " + str(block.trials[0].secondQuestionAnswer))
                #print("b")
                verbDiff = abs(block.verbCount -  block.trials[0].firstQuestionAnswer)
                nounDiff = abs(block.nounCount - block.trials[0].secondQuestionAnswer)
            else:
                #print("c")
                #print(str(block.verbCount) + " " + str(block.trials[0].secondQuestionAnswer))
                #print(str(block.nounCount) + " " + str(block.trials[0].firstQuestionAnswer))
                #print("d")
                verbDiff = abs(block.verbCount -  block.trials[0].secondQuestionAnswer)
                nounDiff = abs(block.nounCount - block.trials[0].firstQuestionAnswer)
            self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_VERB_DIFFERENCE,verbDiff)
            self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_NOUN_DIFFERENCE,nounDiff)
            if(verbDiff == 0 and nounDiff == 0):
                self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_ACCURACY,1)
            else:
                self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_ACCURACY,0)
        self.blockSheetRow += 1

        for trial in block.trials:
            self.printTrail(trial)

    def printTrail(self,trial):
        if(trial.isDummy()):
            self.switchSheetRow += 1
            return
        if(trial.isSwitch()):
            self.switchSheet.write(self.switchSheetRow, Excel.SWITCH_SWITCH, 1)
        else:
             self.switchSheet.write(self.switchSheetRow, Excel.SWITCH_SWITCH, 0)
        if(trial.type == '1'):
            if(trial.category == 'Neut'):
                if(trial.lastCategory == 'Neut'):
                    self.switchSheet.write(self.switchSheetRow, Excel.SWITCH_TYPE, 1)
                else:
                    self.switchSheet.write(self.switchSheetRow, Excel.SWITCH_TYPE, 2)
            else:
                if(trial.lastCategory == 'Neut'):
                    self.switchSheet.write(self.switchSheetRow, Excel.SWITCH_TYPE, 4)
                else:
                    self.switchSheet.write(self.switchSheetRow, Excel.SWITCH_TYPE, 3)
        self.switchSheetRow += 1

    def SwitchSheetTitles(self):
        self.switchSheet.write(0, Excel.SWITCH_SWITCH, 'switch')
        self.switchSheet.write(0, Excel.SWITCH_TYPE, 'type')

        #meta data table in switch sheet:
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
        self.blocksSheet.write(0, Excel.BLOCKS_USER_NUMBER, 'User number')
        self.blocksSheet.write(0, Excel.BLOCKS_VERSION, 'version')
        self.blocksSheet.write(0, Excel.BLOCKS_BLOCK_NUMBER, 'block number')
        self.blocksSheet.write(0, Excel.BLOCKS_NEUT_DIFFERENCE, 'Neut difference')
        self.blocksSheet.write(0, Excel.BLOCKS_EMO_DIFFERENCE, 'Emo difference')
        self.blocksSheet.write(0, Excel.BLOCKS_VERB_DIFFERENCE, 'Verb difference')
        self.blocksSheet.write(0, Excel.BLOCKS_NOUN_DIFFERENCE, 'Noun difference')
        self.blocksSheet.write(0, Excel.BLOCKS_ACCURACY, 'Accuracy')

    def timingSheetTitles(self):
        self.timingSheet.merge_range('B1:D1', 'Neutral version', self.merge_format)
        self.timingSheet.merge_range('E1:K1', 'Emotional version', self.merge_format)

        self.timingSheet.write(1,Excel.TIMIMNG_SUBJECT_ID, 'subject id')
        self.timingSheet.write(1,Excel.TIMING_S_NEUTRAL, 'S - Neutral')
        self.timingSheet.write(1,Excel.TIMING_NS_NEUTRAL, 'NS - Neutral')
        self.timingSheet.write(1,Excel.TIMING_ISC_NEUTRAL, 'ISC - Neutral')
        self.timingSheet.write(1,Excel.TIMING_N_N_EMOTINAL, 'N-N - Emotinal')
        self.timingSheet.write(1,Excel.TIMING_N_E_EMOTINAL, 'N-E - Emotinal')
        self.timingSheet.write(1,Excel.TIMING_E_N_EMOTINAL, 'E-N - Emotinal')
        self.timingSheet.write(1,Excel.TIMIMNG_E_E_EMOTINAL, 'E-E - Emotinal')
        self.timingSheet.write(1,Excel.TIMIMNG_S_EMOTINAL, 'S - Emotinal')
        self.timingSheet.write(1,Excel.TIMIMNG_NS_EMOTINAL, 'NS - Emotinal')
        self.timingSheet.write(1,Excel.TIMING_ISC_EMOTINAL, 'ISC - Emotinal')

    def close(self):
        self.workbook.close()