import xlsxwriter
import datetime

class Excel:
    timingSheetRow = 2
    blockSheetRow = 1
    switchSheetRow = 1

    #column numbers in trials sheet - consts
    TRIALS_USER_ID = 0
    TRIALS_TIMING = 1
    TRIALS_SWITCH = 2
    TRIALS_TYPE = 3
    TRIALS_STANDARD_DEVIATION = 4

    #column numbers in block sheet - consts
    BLOCKS_USER_NUMBER = 0
    BLOCKS_VERSION = 1
    BLOCKS_BLOCK_NUMBER = 2
    BLOCKS_NEUT_DIFFERENCE = 3
    BLOCKS_EMO_DIFFERENCE = 4
    BLOCKS_VERB_DIFFERENCE = 5
    BLOCKS_NOUN_DIFFERENCE = 6
    BLOCKS_ACCURACY = 7
    BLOCKS_ACCURACY_SWITCH = 8
    BLOCKS_ACCURACY_01 = 9
    BLOCKS_ACCURACY_SWITCH_01 = 10

    #column numbers in users sheet - consts
    USERS_SUBJECT_ID = 0
    USERS_S_NEUTRAL = 1
    USERS_NS_NEUTRAL = 2
    USERS_ISC_NEUTRAL = 3
    USERS_N_N_EMOTINAL = 4
    USERS_N_E_EMOTINAL = 5
    USERS_E_N_EMOTINAL = 6
    USERS_E_E_EMOTINAL = 7
    USERS_S_EMOTINAL = 8
    USERS_NS_EMOTINAL = 9
    USERS_ISC_EMOTINAL = 10
    USERS_MEAN = 11
    USERS_STANDARD_DEVIATION = 12
    USERS_ACCURACY = 13
    USERS_ACCURACY_SWITCH = 14
    USERS_ACCURACY_01 = 15
    USERS_ACCURACY_SWITCH_01 = 16

    def __init__(self,fileName):
        self.workbook = xlsxwriter.Workbook(fileName)
        self.merge_format = self.workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'})

        self.metaSheet = self.workbook.add_worksheet('Meta data')
        self.taskSheet = self.workbook.add_worksheet('Task')
        self.usersSheet = self.workbook.add_worksheet('Users')
        self.blocksSheet = self.workbook.add_worksheet('Blocks')
        self.trialsSheet = self.workbook.add_worksheet('Trials')

        #add titles for all the sheets
        self.metaSheetTitles()
        self.trialsSheetTitles()
        self.blocksSheetTitles()
        self.usersSheetTitles()

    def printTask(self,task):
        self.taskSheet.write(0,0,'standard score')
        self.taskSheet.write(0, 1, task.standardScore)

        self.taskSheet.write(1,0,'rate')
        self.taskSheet.write(1, 1, task.standardScoreRate)

        self.taskSheet.write(3,0,'Accuracy rates:')
        self.taskSheet.write(4,0,'Accuracy')
        self.taskSheet.write(4, 1, task.accuracyRate)
        self.taskSheet.write(5,0,'Accuracy(include switch)')
        self.taskSheet.write(5, 1, task.accuracySwitchRate)
        self.taskSheet.write(6,0,'Accuracy(+-1)')
        self.taskSheet.write(6, 1, task.accuracy01Rate)
        self.taskSheet.write(7,0,'Accuracy(include switch and +-1)')
        self.taskSheet.write(7, 1, task.accuracySwitch01Rate)
        for user in task.users:
            self.printUser(user)

    def printUser(self,user):
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_SUBJECT_ID, user.id)
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_S_NEUTRAL, user.neutral_S.getMean())
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_NS_NEUTRAL, user.neutral_NS.getMean())
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_ISC_NEUTRAL, user.neutral_S - user.neutral_NS)
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_N_N_EMOTINAL, user.emotional_NN.getMean(1))
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_N_E_EMOTINAL, user.emotional_NE.getMean(1))
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_E_N_EMOTINAL, user.emotional_EN.getMean(1))
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_E_E_EMOTINAL, user.emotional_EE.getMean(1))
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_S_EMOTINAL, user.emotional_S.getMean())
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_NS_EMOTINAL, user.emotional_NS.getMean())
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_ISC_EMOTINAL, user.emotional_S - user.emotional_NS)
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_MEAN, user.mean)
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_STANDARD_DEVIATION, user.standardDeviation)
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_ACCURACY, user.accuracyRate)
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_ACCURACY_SWITCH, user.accuracySwitchRate)
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_ACCURACY_01, user.accuracy01Rate)
        self.usersSheet.write(self.timingSheetRow, Excel.USERS_ACCURACY_SWITCH_01, user.accuracySwitch01Rate)

        self.timingSheetRow += 1

        for block in user.blocks:
            if(len(block.trials) == 0):
                continue
            self.printBlock(block)

    def printBlock(self,block):
        self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_USER_NUMBER, block.userId)
        self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_VERSION, block.type)
        self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_BLOCK_NUMBER, block.id)
        if(block.type == '1'): # emo - neut block
            self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_EMO_DIFFERENCE, block.emoDiff)
            self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_NEUT_DIFFERENCE, block.neutDiff)
        else: # verb - noun block
            self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_VERB_DIFFERENCE,block.verbDiff)
            self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_NOUN_DIFFERENCE,block.nounDiff)

        self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_ACCURACY,int(block.accuracy))
        self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_ACCURACY_SWITCH,int(block.accuracySwitch))
        self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_ACCURACY_01,int(block.accuracy01))
        self.blocksSheet.write(self.blockSheetRow, Excel.BLOCKS_ACCURACY_SWITCH_01,int(block.accuracySwitch01))

        self.blockSheetRow += 1

        for trial in block.trials:
            self.printTrial(trial)

    def printTrial(self,trial):
        self.trialsSheet.write(self.switchSheetRow, Excel.TRIALS_USER_ID, trial.userId)
        self.trialsSheet.write(self.switchSheetRow, Excel.TRIALS_TIMING, trial.timing)

        if(trial.isDummy()):
            self.switchSheetRow += 1
            return
        if(trial.isSwitch()):
            self.trialsSheet.write(self.switchSheetRow, Excel.TRIALS_SWITCH, 1)
        else:
             self.trialsSheet.write(self.switchSheetRow, Excel.TRIALS_SWITCH, 0)
        if(trial.type == '1'):
            if(trial.category == 'Neut'):
                if(trial.lastCategory == 'Neut'):
                    self.trialsSheet.write(self.switchSheetRow, Excel.TRIALS_TYPE, 1)
                else:
                    self.trialsSheet.write(self.switchSheetRow, Excel.TRIALS_TYPE, 2)
            else:
                if(trial.lastCategory == 'Neut'):
                    self.trialsSheet.write(self.switchSheetRow, Excel.TRIALS_TYPE, 4)
                else:
                    self.trialsSheet.write(self.switchSheetRow, Excel.TRIALS_TYPE, 3)

        self.trialsSheet.write(self.switchSheetRow, Excel.TRIALS_STANDARD_DEVIATION, trial.standardScore)

        self.switchSheetRow += 1

    def metaSheetTitles(self):
        self.metaSheet.write(0,0, 'created at')
        self.metaSheet.write(0,1, datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))

        self.metaSheet.merge_range('G1:H1', 'trial switch index', self.merge_format)
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

    def trialsSheetTitles(self):
        self.trialsSheet.write(0, Excel.TRIALS_USER_ID, 'User id')
        self.trialsSheet.write(0, Excel.TRIALS_TIMING, 'Timing')
        self.trialsSheet.write(0, Excel.TRIALS_SWITCH, 'Switch')
        self.trialsSheet.write(0, Excel.TRIALS_TYPE, 'Type')
        self.trialsSheet.write(0, Excel.TRIALS_STANDARD_DEVIATION, 'standard deviations')

    def blocksSheetTitles(self):
        self.blocksSheet.write(0, Excel.BLOCKS_USER_NUMBER, 'User number')
        self.blocksSheet.write(0, Excel.BLOCKS_VERSION, 'version')
        self.blocksSheet.write(0, Excel.BLOCKS_BLOCK_NUMBER, 'block number')
        self.blocksSheet.write(0, Excel.BLOCKS_NEUT_DIFFERENCE, 'Neut difference')
        self.blocksSheet.write(0, Excel.BLOCKS_EMO_DIFFERENCE, 'Emo difference')
        self.blocksSheet.write(0, Excel.BLOCKS_VERB_DIFFERENCE, 'Verb difference')
        self.blocksSheet.write(0, Excel.BLOCKS_NOUN_DIFFERENCE, 'Noun difference')
        self.blocksSheet.write(0, Excel.BLOCKS_ACCURACY, 'Accuracy')
        self.blocksSheet.write(0, Excel.BLOCKS_ACCURACY_SWITCH, 'Accuracy(include switch)')
        self.blocksSheet.write(0, Excel.BLOCKS_ACCURACY_01, 'Accuracy (up to 1 difference)')
        self.blocksSheet.write(0, Excel.BLOCKS_ACCURACY_SWITCH_01, 'Accuracy (include switch and up to 1 difference)')

    def usersSheetTitles(self):
        self.usersSheet.merge_range('B1:D1', 'Neutral version', self.merge_format)
        self.usersSheet.merge_range('E1:K1', 'Emotional version', self.merge_format)
        self.usersSheet.merge_range('L1:M1', 'Statistics', self.merge_format)
        self.usersSheet.merge_range('N1:Q1', 'Accuracy', self.merge_format)

        self.usersSheet.write(1, Excel.USERS_SUBJECT_ID, 'Subject id')
        self.usersSheet.write(1, Excel.USERS_S_NEUTRAL, 'S - Neutral')
        self.usersSheet.write(1, Excel.USERS_NS_NEUTRAL, 'NS - Neutral')
        self.usersSheet.write(1, Excel.USERS_ISC_NEUTRAL, 'ISC - Neutral')
        self.usersSheet.write(1, Excel.USERS_N_N_EMOTINAL, 'N-N - Emotinal')
        self.usersSheet.write(1, Excel.USERS_N_E_EMOTINAL, 'N-E - Emotinal')
        self.usersSheet.write(1, Excel.USERS_E_N_EMOTINAL, 'E-N - Emotinal')
        self.usersSheet.write(1, Excel.USERS_E_E_EMOTINAL, 'E-E - Emotinal')
        self.usersSheet.write(1, Excel.USERS_S_EMOTINAL, 'S - Emotinal')
        self.usersSheet.write(1, Excel.USERS_NS_EMOTINAL, 'NS - Emotinal')
        self.usersSheet.write(1, Excel.USERS_ISC_EMOTINAL, 'ISC - Emotinal')
        self.usersSheet.write(1, Excel.USERS_MEAN, 'Mean')
        self.usersSheet.write(1, Excel.USERS_STANDARD_DEVIATION, 'Standard deviation')
        self.usersSheet.write(1, Excel.USERS_ACCURACY, 'Accuracy')
        self.usersSheet.write(1, Excel.USERS_ACCURACY_SWITCH, 'Accuracy(include switch)')
        self.usersSheet.write(1, Excel.USERS_ACCURACY_01, 'Accuracy(+-1)')
        self.usersSheet.write(1, Excel.USERS_ACCURACY_SWITCH_01, 'Accuracy(include switch and +-1)')



    def close(self):
        self.workbook.close()