import os


def path_generator(mode):
    file = open('word_'+mode)
    path = []
    for line in file:
        line = line[:-1]
        kw_sep = line.split(' ')
        kw_reassemble = ''
        for kwsep in kw_sep:
            kw_reassemble += '+' + kwsep
        kw_reassemble = kw_reassemble[1:]

        path = '/Users/yipengm/PycharmProjects/AMZ_LIB/' + date + '/' + mode + '/' + kw_reassemble + '_collect/'

##single product single ASIN single date
#input: path to date/product
#output: none directly write a file
def SPSA(path,ASIN,date):
    fw = open(ASIN+'Rank'+date,'w+')
    print('word,page,Count,isAd,note',file = fw)
    wordsCollect = os.listdir(path)
    wordsCollect.sort()
    for word in wordsCollect:
        wordDir = path+'/'+word
        singleWordAllPages = os.listdir(wordDir)
        singleWordAllPages.sort()
        page = 0
        iffound = 0
        for fileLine in singleWordAllPages:
            singleWordSinglePages = wordDir+'/'+fileLine
            wordName = fileLine[:-10]
            f = open(singleWordSinglePages)
            count = 0
            adCount = 0
            normalCount = 0
            page += 1
            for line in f:
                line = line[:-1]
                lineSp = line.split(',')
                ASINCur = lineSp[0].split(':')[1]
                isAd = lineSp[1].split(':')[1]
                count += 1
                if int(isAd) == 1:
                    adCount += 1
                else:
                    normalCount += 1
                if ASINCur == ASIN and int(isAd) == 1:
                    linePrint = wordName+',' + str(page) + ',' + str(count) + ',1,adcount:'+str(adCount)
                    print(linePrint,file=fw)
                    iffound = 1
                elif ASINCur == ASIN:
                    linePrint = wordName + ',' + str(page) + ',' + str(count) + ',0,normalcount:'+str(normalCount)
                    print(linePrint,file=fw)
                    iffound = 1

            ##if iffound > 0 :
            ##    break




if __name__ == "__main__":

    for date in ['_01_01_19','_01_02_19','_01_03_19','_01_04_19','_12_30_19','_12_31_19','_01_04_11']:
        #for ASIN in ['B08RD2SDRB','B09KBND44B','B08ZN2JNPY','B09FPGML3V','B07L6RXDJ6','B08XYPP3FQ']:
        for ASIN in [ 'B09KBND44B', 'B095SPX6B9']:
            SPSA('/Users/yipengm/PycharmProjects/amz_analysis/MM' + date, ASIN, date)






