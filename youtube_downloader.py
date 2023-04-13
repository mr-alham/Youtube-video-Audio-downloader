
#!/usr/bin/env python3

'''This Python script allows you to download videos and audios from YouTube by simply entering the URL of the video.
It uses the PyTube library to download the desired format of the video or audio.
The script has a colorful terminal output.
*** curently this will only work on only linux as intended '''


import subprocess
import sys
from pytube import YouTube
import clipboard
from os import getlogin as user_name
import os


def color(color):
    '''ansi color codes to get colored output on termainl'''

    colors = {'reset': '\033[0m',
              'red': '\033[31m',
              'green': '\033[32m',
              'yellow': '\033[33m',
              'blue': '\033[34m',
              'white': '\033[37m',
              'bold': '\033[1m',
              'underlined': '\033[4m',
              'italic': '\033[3m'}

    string = ''

    for clr in color:
        string += colors[clr]

    return str(string)


class ytube():
    try:
        def __init__(self, link):
            self.link = link
            self.yt = YouTube(link)

        def title(self):
            yt = self.yt
            return f'{color(["bold","blue"])}Title: {color(["reset","blue","italic"])}{yt.title}{color(["reset"])}'
    except:
        print(f'{color(["red"])}an error occurred!{color(["reset"])}')

    def download_path(self):
        '''determine the download path on each operating system to download and if couldn't download on current working direcotory'''

        if os.name == 'nt':
            download_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        elif os.name == 'posix' and 'darwin' in os.uname().sysname.lower():
            download_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        elif os.name == 'posix' and 'linux' in os.uname().sysname.lower():
            download_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        else:
            download_path = '.'

        return download_path

    def Video(self):
        '''if wanted to download the youtube video processes for that will happen here'''

        yt = self.yt

        streams = {1: '144p',
                   2: '240p',
                   3: '360p',
                   4: '480p',
                   5: '720p',
                   6: '1080p', }

        streams_itag = {
            "1": 17,
            "2": 133,
            "3": 18,
            "4": 135,
            "5": 22,
            "6": 137
        }

        print()

        for stream in streams:
            print(f'\t{color(["bold","red"])}{stream}. {color(["reset","green"])}{streams[stream]}')

        video_format = input(f'choose a video stream to download.(press enter for 360p): ')

        print(f'downloading{color(["white","bold"])}.{color(["blue"])}.{color(["green"])}.{color(["reset","green"])}')

        if video_format == '':
            video_format = '3'

        video = yt.streams.get_by_itag(str(streams_itag[video_format]))

        video.download(self.download_path())

        print(f'downloaded on {color(["blue","italic"])}{self.download_path()}')

        sys.exit()

    def Audio(self):
        '''if want to download only audio from youtube video processes for that will happen here'''
        
        yt = self.yt
        print(f'downloading{color(["white","bold"])}.{color(["blue"])}.{color(["green"])}.{color(["reset","green"])}')

        audio = yt.streams.get_audio_only()

        file_location = str(audio.download(self.download_path())).replace(' ', '\x20')

        mp3_file_locaton = file_location[:file_location.rfind('.')]+'.mp3'

        try:

            '''when we try to download audio version through pytube we can\'t download as mp3. so in here converting mp4 into mp3'''

            ffmpeg_cmd = ["ffmpeg", "-i", file_location, "-vn", "-acodec","libmp3lame", "-b:a", "192k", "-loglevel", "error", mp3_file_locaton]
            subprocess.check_output(ffmpeg_cmd, stderr=subprocess.STDOUT)
            subprocess.run(["gio", "trash", file_location])

            print('Successfully converted to mp3')

        except subprocess.CalledProcessError as e:
            print('Error during converting mp4 to mp3:', e.output.decode())

        print(
            f'downloaded on {color(["blue","italic"])}{self.download_path()}')

        sys.exit()


def welcome():
    print(f'{color(["bold","green"])}Youtube {color(["underlined","italic"])}Video/Audio{color(["reset","bold","green"])} Downloader by {color(["white","italic"])}Alham_{color(["red"])}\U0000270C{color(["reset"])}')

    link = str(input(f'enter url {color(["italic"])}(enter to copy from clipboard){color(["reset"])}: '))
    
    if link == '':
        link = clipboard.paste()

    utube = ytube(link)

    print(utube.title())
    
    def decision():
        decs = input(f'{color(["red","bold"])}\
    1. {color(["reset","green"])}Video{color(["reset"])}\n{color(["red","bold"])}\
    2. {color(["reset","green"])}Audio\nselect a format(press enter for Audio): ')
        return decs

    decs = str(decision())
    if decs == '1':
        utube.Video()
    elif decs == '2' or decs == '':
        utube.Audio()
    else:
        decs = decision()
        if decs == '1':
            utube.Video()
        elif decs == '2' or decs == '':
            utube.Audio()
        else:
            print(f'couldn\'t recognize the request')


def check_internet_connection():
    try:
        output = subprocess.check_output(['ping', '-c', '1', 'google.com'])
        return True
    except subprocess.CalledProcessError:
        return False


if check_internet_connection():
    try:
        welcome()
    except ImportError:
        print('if you didn\'t install these modules import\n * pytube \n * clipboard')
    except AttributeError:
        print('invalid url')
    except KeyboardInterrupt:
        print('\naborting!')
        sys.exit()
    except KeyError:
        print('invalied stream number')
    except Exception as e:
        print(f'{color(["red"])}an error occurred!{color(["reset"])}')
        print(e)
else:
    print('you don\'t hava an active internet connection')
