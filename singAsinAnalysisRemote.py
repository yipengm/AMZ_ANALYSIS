import os
import paramiko
import sys
###not finished
import getopt
from singProductInfo import singProductInfo



#paramiko setup
info = singProductInfo()
hostname = info.hostname
port = info.port
username = info.username
password = info.password

#info.setAsin(['B09KBND44B','B08RD2SDRB','B07L6RXDJ6','B08RD4FK54','B09FPGML3V','B092QVGQMM','B08ZN2JNPY','B08XYPP3FQ','B083M4DV54'])
#info.setAsin(['B08BRL8WGJ','B076J7WSPP','B07Z6BLBLP','B07QKX6X5P','B09M8CNR4P','B098T3VCHV','B092HWKGS2','B0948XFX9P','B09DSQG1J8','B09CCXSMRP','B081TW9WTD'])
#info.setAsin(['B09HS962VT','B09234GQXV','B097B9TSKN','B0925SW3CP','B099WGH259','B09BNGXQP1','B09GM6B6CJ','B09535CQWV','B097MHQGC3'])

MMset = ['B09KBND44B','B08RD2SDRB','B07L6RXDJ6','B08RD4FK54','B09FPGML3V','B092QVGQMM','B08ZN2JNPY','B08XYPP3FQ','B083M4DV54','B09B3SQ1CG','B09BCC4W1F','B09M6DP1CN','B08PBMN2ZF','B08ZHR8MYW']
BHset = ['B08BRL8WGJ','B08RNQNFW1','B07Z6BLBLP','B076J7WSPP','B0948XFX9P','B08XJS3RQ6','B09CCXSMRP','B07QKX6X5P','B09HCFD9WC','B09GTY1CF2','B09F3HQHNN']
PBset = ['B08CZPV43C','B08V956FZ6','B09YNK5T16','B084P3FJKL','B09F5YT5MV','B07QC7SXJL','B004P2OLB8','B07NSSCCLY','B09B8NFC9N','B0969VR8H5']
SBset = ['B09WYG8RFR','B09WYH432Y']


#info.setAsin()
#info.setAsin(BHset)

def lscmd(sftp,path):
    outline = sftp.listdir(path)
    return outline


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
        path = '/E:/luosi_data/' + date.replace(':','_') + '/' + mode + '/' + kw_reassemble + '_collect/'

##single product single ASIN single date
#input: path to date/product
#output: none; directly write a file

if __name__ == "__main__":
    date = 'none'
    mode = 'none'
    luosiDataPath = '/E:/luosi_data/'
    try:
        date = sys.argv[2]
        mode = sys.argv[4]
    except getopt.GetoptError:
        print('test.py -d <date> -m <mode>')
        sys.exit(2)
    print('date：', date)
    print('mode：', mode)
    dateSplit = date.split('/')
    singleDayIter = int(int(dateSplit[0].split(':')[0])/4)
    info.setProduct(mode)

    if mode == 'MM':
        info.setAsin(MMset)
    elif mode == 'BH':
        info.setAsin(BHset)
    elif mode == 'PB':
        info.setAsin(PBset)

    #date = 'PST_'+dateSplit[3]+'_'+dateSplit[1]+'_'+dateSplit[2]+'_'+str(singleDayIter)+'_'+dateSplit[0]
    date = 'PST_'+dateSplit[3]+'_'+dateSplit[1]+'_'+dateSplit[2]
    PST_date = dateSplit[0]
    info.setDate(date)


    #generate datastr

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password,port=port)
    sftp = ssh.open_sftp()

    outline = sftp.listdir(luosiDataPath)

    for line in outline:
        if line.startswith(date,0):
            time = line
            info.addTime(time)

    fWord = open('word_'+mode)
    for word in fWord:
        word = word[:-1]
        word = word.replace(' ','+')
        info.addWord(word)

    #info.loadTAWL()
    info.update()
    info.generateTop()
    info.printTime_ASINWord()
    info.printASIN_timeWord()
    info.printWord_ASINTime()

    print('done')
    #
    #SPSA('/Users/yipengm/PycharmProjects/AMZ_LIB/PST_2021_12_25_1_12_00/MM_01_01_19')








