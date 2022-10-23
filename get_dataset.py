import requests
from bs4 import BeautifulSoup
import os
from time import sleep
from pySmartDL import SmartDL


base_url = 'https://bluearchive.wiki'
base_dir = os.getcwd()

def GetCharacter():
    r = requests.get('https://bluearchive.wiki/wiki/Category:Characters_audio')
    soup = BeautifulSoup(r.text, 'html.parser')

    a = soup.find('div', {'class':'mw-category mw-category-columns'}).find_all('a')

    f = open('url.txt', 'w', encoding='utf-8')

    for i in a:
        url = base_url+i['href'] 
        title = i['title']
        print(url)
        
        dir_path = f"./blue_archive/{title.split(' ')[0].split('/')[0]}/"
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        if not os.path.isdir(dir_path+'wavs/'):
            os.mkdir(dir_path+'wavs/')
        if not os.path.isdir(dir_path+'oggs/'):
            os.mkdir(dir_path+'oggs/')

        f.writelines(f'{url}|{dir_path}\n')


def download_ogg(oggUrl, oggdir):
    while True:
        try:
            obj = SmartDL(oggUrl, f'{oggdir}/oggs/')
            obj.start()
            path = obj.get_dest()
            break
        except:
            print("1초 후 다시 요청")
            sleep(1)



def set_sample_rate(oggdir):
    os.chdir(f'{oggdir}/oggs/'.replace('//', '/'))
    os.system('FOR /F "tokens=*" %G IN (\'dir /b *.ogg\') DO ffmpeg -i "%G" -ac 1 -ar 22050 "../wavs/%~nG.wav" ')
    os.chdir(base_dir)


def DownloadData():
    f = open('url.txt', 'r', encoding='utf-8').read().split('\n')[2:]
    for idx, i in enumerate(f):
        url, oggdir = i.split('|')
        
        print(f'\n{idx}', oggdir)
        print('-------------------------------------------')
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        audio_file = soup.find_all('source', {'data-shorttitle':'Ogg source'})

        for ogg in audio_file:
            link = 'https:'+ogg['src']
            print(link)
            download_ogg(link, oggdir)
        
        set_sample_rate(oggdir)

        print(os.getcwd())
        print('\n')
        # break



DownloadData()