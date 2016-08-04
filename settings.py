class settings:
    dataFileName = ''
    dataFileEncoding = ''
    dataFileVariablesLine = -1

    excelFileName = ''
    def readSettingsFile(self):
        try:
            f = open('settings.txt','r')
            lines = f.readlines()
            for line in lines:
                if(line.startswith('//')):
                    continue
                if(len(line)<2):
                    continue
                (var,value) = line.split(':')
                if(var == 'data_file'):
                    self.dataFileName = value.strip('\n')
                elif(var == 'encoding'):
                    self.dataFileEncoding = value.strip('\n')
                elif(var == 'variables_name_line'):
                    self.dataFileVariablesLine = (int)(value.strip('\n')) - 1
                elif(var == 'excel_file'):
                    self.excelFileName = value.strip('\n')
        except:
            print('Failed to open setting file')
            exit()

        f.close()
        if(self.dataFileName == '' or self.dataFileEncoding == '' or self.dataFileVariablesLine == -1 or self.excelFileName == ''):
            print('Failed to parse setting file')
            exit()


