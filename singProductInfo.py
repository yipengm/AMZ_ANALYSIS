import paramiko
import numpy as np
import xlwt
from xlwt import Workbook

class singleLoc:
    def __init__(self,page,count,ifAd,adCount,normalCount):
        self.page = page
        self.count = count
        self.ifAd = ifAd
        self.adCount = adCount
        self.normalCount = normalCount


class singProductInfo:
    def __init__(self):
        self.luosiDataPath = '/E:/luosi_data/'
        self.hostname = '192.168.3.12'
        self.date = 'PST_0000_00_00'
        self.port = 22
        self.username = 'Administrator'
        self.password = 'Wo12345!'
        self.product = 'BH'
        self.asinList = []
        self.timeList = []
        self.wordList = []
        self.wordDict = dict()
        self.timeDict = dict()
        self.ASINDict = dict()
        self.TAWL = 1
        self.TAWL_top = 1
        self.TAWL_ad = 1
        self.TAWL_normal = 1

    def setDate(self,date):
        self.date = date

    def setAsin(self,asinList):
        for asin in asinList:
            self.appendAsin(asin)

    def resetAsin(self):
        self.asinList = []
        self.ASINDict.clear()

    def appendAsin(self,asin):
        self.ASINDict[asin] = len(self.asinList)
        self.asinList.append(asin)

    def setHost(self, hostname):
        self.hostname=hostname

    def setPort(self, port):
        self.port=port

    def setUsername(self, username):
        self.username=username

    def setPassword(self, password):
        self.password=password

    def setProduct(self,product):
        self.product = product

    def setTime(self,timeList):
        self.timeList = timeList

    def addTime(self,time):
        self.timeDict[time] = len(self.timeList)
        self.timeList.append(time)

    def resetTime(self):
        self.timeList.clear()
        self.timeDict.clear()

    def addWord(self,word):
        self.wordDict[word] = len(self.wordList)
        self.wordList.append(word)


    def resetWord(self):
        self.wordList.clear()
        self.wordDict.clear()

    def setWord(self,wordList):
        self.wordList = wordList



    def update(self):
        ##TAWL
        timeSize = len(self.timeList)
        asinSize = len(self.asinList)
        wordSize = len(self.wordList)
        TAWL_temp = np.ones([timeSize,asinSize,wordSize,5,2])*1000
        #TAWL_normal_temp = [[[dummyLoc for i in range(wordSize)] for j in range(asinSize)] for k in range(timeSize)]
        #TAWL_ad_temp = [[[dummyLoc for i in range(wordSize)] for j in range(asinSize)] for k in range(timeSize)]

        for timeInd in range(len(self.timeList)):
            print('running'+self.timeList[timeInd])
            pathRemote = self.luosiDataPath + self.timeList[timeInd] + '/' + self.product + '/'
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.hostname, username=self.username, password=self.password,port=self.port)
            sftp = ssh.open_sftp()
            outline = sftp.listdir(pathRemote)
            outline.sort()

            for line in outline:
                line = line
                wordDir = pathRemote + line
                try:
                    singleWordAllPages = sftp.listdir(wordDir)
                except:
                    print('error'+wordDir)
                    continue
                singleWordAllPages.sort()
                page = 0
                for fileLine in singleWordAllPages:
                    fileLine = fileLine
                    singleWordSinglePages = wordDir + '/' + fileLine
                    wordName = fileLine[:-10]
                    if wordName in self.wordDict.keys():
                        wordInd = self.wordDict[wordName]
                    else:
                        continue
                    singleWordSinglePages = singleWordSinglePages.replace('\\','')
                    f = sftp.open(singleWordSinglePages)
                    count = 0
                    adCount = 0
                    normalCount = 0
                    page += 1
                    for line in f:
                        line = line[:-1]
                        lineSp = line.split(',')
                        ASINLine = lineSp[0].split(':')[1]
                        isAd = lineSp[1].split(':')[1]
                        count += 1
                        if int(isAd) == 1:
                            adCount += 1
                        else:
                            normalCount += 1

                        if ASINLine in self.ASINDict.keys():
                            ASINInd = self.ASINDict[ASINLine]
                            if int(isAd) == 1:
                                TAWL_temp[timeInd, ASINInd, wordInd, 0, 0] = page
                                TAWL_temp[timeInd, ASINInd, wordInd, 1, 0] = count
                                TAWL_temp[timeInd, ASINInd, wordInd, 2, 0] = int(isAd)
                                TAWL_temp[timeInd, ASINInd, wordInd, 3, 0] = adCount
                                TAWL_temp[timeInd, ASINInd, wordInd, 4, 0] = normalCount
                            else:
                                TAWL_temp[timeInd, ASINInd, wordInd, 0, 1] = page
                                TAWL_temp[timeInd, ASINInd, wordInd, 1, 1] = count
                                TAWL_temp[timeInd, ASINInd, wordInd, 2, 1] = int(isAd)
                                TAWL_temp[timeInd, ASINInd, wordInd, 3, 1] = adCount
                                TAWL_temp[timeInd, ASINInd, wordInd, 4, 1] = normalCount
                    f.close()

        self.TAWL = TAWL_temp
        np.save('/Users/yipengm/PycharmProjects/amz_analysis/'+self.date+'TAWL_'+self.product+'.npy',self.TAWL)

    def generateTop(self):
        self.TAWL_ad = self.TAWL[:,:,:,:,0]
        self.TAWL_normal = self.TAWL[:,:,:,:,1]
        TAWL_bool0 = self.TAWL_ad[:, :, :, 0:1] > self.TAWL_normal[:, :, :, 0:1]
        TAWL_bool1 = self.TAWL_ad[:, :, :, 0:1] < self.TAWL_normal[:, :, :, 0:1]
        TAWL_bool2 = self.TAWL_ad[:, :, :, 0:1] == self.TAWL_normal[:, :, :, 0:1]
        TAWL_bool3 = self.TAWL_ad[:, :, :, 1:2] > self.TAWL_normal[:, :, :, 1:2]
        self.TAWL_top = TAWL_bool0 * self.TAWL_normal + TAWL_bool1 * self.TAWL_ad + \
            TAWL_bool2*TAWL_bool3*self.TAWL_normal+TAWL_bool2*(1-TAWL_bool3)*self.TAWL_ad

        ##TAWL_temp = np.zeros([timeSize,asinSize,wordSize,5,2])

    def printTime_ASINWord(self):
        wb = Workbook()
        # add_sheet is used to create sheet.

        for time in self.timeList:
            sheettemp = wb.add_sheet(time.replace(':','_'))
            timeInd = self.timeDict[time]
            for AID in range(len(self.asinList)):
                sheettemp.write(0,AID+1,self.asinList[AID])

            for WID in range(len(self.wordList)):
                sheettemp.write(WID+1,0,self.wordList[WID].replace('+',' '))

            for ASIN in self.asinList:
                if ASIN in self.ASINDict:
                    ASINInd = self.ASINDict[ASIN]
                    for i in range(len(self.wordList)):
                        page = int(self.TAWL_top[timeInd, ASINInd, i, 0])
                        count = int(self.TAWL_top[timeInd, ASINInd, i, 1])
                        ad = int(self.TAWL_top[timeInd, ASINInd, i, 2])

                        page_str = str(page).zfill(2)
                        count_str = str(count).zfill(3)
                        ad_str = str(ad).zfill(1)

                        if page != 1000:
                            if i == 5 and ASINInd == 8:
                                print('a')
                            sheettemp.write(i+1,ASINInd+1,page_str+'|'+count_str+'|'+ad_str)

        wb.save(self.date+'_'+self.product+'_Time_ASINWORD.xls')

    def printASIN_timeWord(self):
        wb = Workbook()
        # add_sheet is used to create sheet.
        for ASIN in self.asinList:
            if ASIN in self.ASINDict:
                ASINInd = self.ASINDict[ASIN]
                sheettemp = wb.add_sheet(ASIN)

                for TID in range(len(self.timeList)):
                    sheettemp.write(0, TID + 1, self.timeList[TID].replace(':', '_')[-8:])

                for WID in range(len(self.wordList)):
                    sheettemp.write(WID + 1, 0, self.wordList[WID].replace('+', ' '))

                for time in self.timeList:
                    timeInd = self.timeDict[time]
                    for i in range(len(self.wordList)):
                        page = int(self.TAWL_top[timeInd, ASINInd, i, 0])
                        count = int(self.TAWL_top[timeInd, ASINInd, i, 1])
                        ad = int(self.TAWL_top[timeInd, ASINInd, i, 2])

                        page_str = str(page).zfill(2)
                        count_str = str(count).zfill(3)
                        ad_str = str(ad).zfill(1)

                        if page != 1000:
                            sheettemp.write(i + 1, timeInd + 1, page_str + '|' + count_str + '|' + ad_str)

        wb.save(self.date+'_'+self.product+'_ASIN_timeWord.xls')

    def printWord_ASINTime(self):
        wb = Workbook()
        # add_sheet is used to create sheet.
        for i in range(len(self.wordList)):
            sheettemp = wb.add_sheet('word'+str(i))
            sheettemp.write(0,0,self.wordList[i].replace('+', ' '))

            for AID in range(len(self.asinList)):
                sheettemp.write(0,AID+1,self.asinList[AID])

            for TID in range(len(self.timeList)):
                sheettemp.write(TID+1,0,self.timeList[TID].replace(':', '_')[-8:])

            for ASIN in self.asinList:
                if ASIN in self.ASINDict:
                    ASINInd = self.ASINDict[ASIN]
                    for time in self.timeList:
                        timeInd = self.timeDict[time]
                        page = int(self.TAWL_top[timeInd, ASINInd, i, 0])
                        count = int(self.TAWL_top[timeInd, ASINInd, i, 1])
                        ad = int(self.TAWL_top[timeInd, ASINInd, i, 2])

                        page_str = str(page).zfill(2)
                        count_str = str(count).zfill(3)
                        ad_str = str(ad).zfill(1)

                        if page != 1000:
                            sheettemp.write(timeInd+1,ASINInd+1,page_str+'|'+count_str+'|'+ad_str)

        wb.save(self.date+'_'+self.product+'_Word_ASINTime.xls')

    def loadTAWL(self):
        self.TAWL = np.load('/Users/yipengm/PycharmProjects/amz_analysis/preloadinfo/'+self.date+'TAWL_'+self.product+'.npy')
        self.generateTop()

