import requests
# Date Time: 2022.3.7
# Author: jing_zhong
# function: Download English-paper by DOI


def GetDownloadUrl(DOI_EnglishPaper):
    BaseWebStation = 'https://sci-hub.se/'
    url = BaseWebStation + DOI_EnglishPaper
    print(url)
    r = requests.get(url)
    result_txt = r.text
    result_list = result_txt.strip('').split('\n')
    # print(result_list)
    myres = ''
    for line in result_list:
        line = line.strip('\n')
        if line.find('<button onclick =') >= 0:
            myres += line
    if myres == '':
        myres = 'No Result!'
    elif myres.find('//') >= 0:
        myres = 'https:' + myres[myres.find('//'):myres.find('?download=true')]
        # First way： button onclick <button οnclick="location.href='//twin.sci-hub.se/6748/d3cada06ce457b96477116e17c8273e5/nguyen2018.pdf?download=true'">↓ save</button>
    elif myres.find('/downloads') >= 0:
        myres = 'https://sci-hub.se' + \
            myres[myres.find('/downloads'):myres.find('?download=true')]
        # Second way： <button οnclick="location.href='/downloads/2021-05-18/9c/ananias2021.pdf?download=true'">↓ save</button>
    return myres


def DownloadFileByUrl(DownloadUrl):
    # root_download = "download/"
    if DownloadUrl != '' and DownloadUrl.find('http') >= 0:
        FileName = DownloadUrl.split('/')[-1]
        r1 = requests.get(DownloadUrl)
        if r1:
            with open(FileName, "wb") as code:
                code.write(r1.content)
                print(DownloadUrl + '  File ' + FileName +
                      '  has been downloaded successfully!')
        else:
            print('Failed to download')


# doi_EnglishPaper = 'https://doi.org/10.1038/nature07970'
# paperDownloadUrl = GetDownloadUrl(doi_EnglishPaper)  # doi_EnglishPaper
# DownloadFileByUrl(paperDownloadUrl)
