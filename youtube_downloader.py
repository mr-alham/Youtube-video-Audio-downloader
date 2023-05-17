#!/usr/bin/env python3

'''This Python script allows you to download videos and audios from YouTube by simply entering the URL of the video.
It uses the PyTube library to download the desired format of the video or audio.
The script has a colorful terminal output.
*** curently this will only work on only linux as intended '''


from subprocess import run, check_output, DEVNULL, CalledProcessError, STDOUT
from os import name, path, uname, chdir, rename
import sys
from pytube import YouTube
import clipboard


def color(color):
    '''ansi color codes to get colored output on terminal'''

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


class YTube():
    try:
        def __init__(self, link):
            self.link = link
            self.yt = YouTube(link)

        def title(self):
            '''Fetching the Youtube video caption of given url'''
            yt = self.yt
            return f'{color(["bold","blue"])}Title: {color(["reset","blue","italic"])}{yt.title}{color(["reset"])}'
    except Exception as e:
        print(
            f'{color(["red"])}An error occurred while fetching Title: as {e}{color(["reset"])}')

    def download_path(self):
        '''determine the path of default download directory path on each operating system to download and if couldn't download on current working directory'''

        if name == 'nt':
            download_path = path.join(path.expanduser('~'), 'Downloads')

        elif name == 'posix' and 'darwin' in uname().sysname.lower():
            download_path = path.join(path.expanduser('~'), 'Downloads')

        elif name == 'posix' and 'linux' in uname().sysname.lower():
            download_path = path.join(path.expanduser('~'), 'Downloads')

        else:
            download_path = '.'

        chdir(download_path)
        return download_path

    def thumbnail(self, mp3_filename):
        '''Fetches the thumbnail from the given URL and insert the thumbnail into mp3 file'''
        yt = self.yt

        def download_thumbnail(output_filename):
            '''Downloads the thumbnail'''
            try:
                thumbnail_url = yt.thumbnail_url
                run(['wget', thumbnail_url, '-O', output_filename],
                    stdout=DEVNULL, stderr=DEVNULL)

            except Exception as e:
                print(
                    f'An error occurred while downloading the thumbnail: {e}')

        def insert_thumbnail(mp3_filename, thumbnail_file):
            ''''add the thumbnail to the mp3 file'''
            try:

                # we can't add the thumbnail to existing file and save, so we have to create a temporary file
                temp_file = 'temp.mp3'
                run(['ffmpeg', '-i', mp3_filename, '-i', thumbnail_file, '-map', '0', '-map', '1', '-c',
                               'copy', '-id3v2_version', '3', '-y', temp_file], stdout=DEVNULL, stderr=DEVNULL)

                # after inserting the thumbnail moving image and original files into trash folder and renaming temporary file to original name
                run(['gio', 'trash', thumbnail_file])
                run(["gio", "trash", mp3_filename])
                rename(temp_file, mp3_filename)

            except FileNotFoundError as e:
                print(f'File not found: {e}')
            except Exception as e:
                print(f'An error occurred while inserting thumbnail as: {e}')

        # gets mp3 files name as parameter to insert the thumbnail
        download_thumbnail(mp3_filename + '.jpg')
        insert_thumbnail(mp3_filename, mp3_filename + '.jpg')

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
            print(
                f'\t{color(["bold","red"])}{stream}. {color(["reset","green"])}{streams[stream]}')

        video_format = input(
            f'choose a video stream to download.(press enter for 360p): ')

        print(
            f'downloading{color(["white","bold"])}.{color(["blue"])}.{color(["green"])}.{color(["reset","green"])}')

        if video_format == '':
            video_format = '3'

        video = yt.streams.get_by_itag(str(streams_itag[video_format]))

        video.download(self.download_path())

        print(
            f'downloaded on {color(["blue","italic"])}{self.download_path()}')

        sys.exit()

    def Audio(self):
        '''if want to download only audio from youtube video processes for that will happen here'''

        yt = self.yt
        print(
            f'downloading{color(["white","bold"])}.{color(["blue"])}.{color(["green"])}.{color(["reset","green"])}')

        audio = yt.streams.get_audio_only()

        file_location = str(audio.download(
            self.download_path())).replace(' ', '\x20')

        mp3_file_location = f"{file_location[:file_location.rfind('.')]}.mp3"

        try:
            '''when we try to download audio version through pytube we can\'t download as mp3. so in here converting mp4 into mp3'''

            ffmpeg_cmd = ["ffmpeg", "-i", file_location, "-vn", "-acodec",
                          "libmp3lame", "-b:a", "192k", "-loglevel", "error", mp3_file_location]
            check_output(ffmpeg_cmd, stderr=STDOUT)
            run(["gio", "trash", file_location])

            print('Successfully converted to mp3')

            # inserting the thumbnail to the downloaded mp3 file
            self.thumbnail(mp3_file_location)

        except CalledProcessError as e:
            print('Error during converting mp4 to mp3:', e.output.decode())

        print(
            f'downloaded on {color(["blue","italic"])}{self.download_path()}')


def welcome():
    print(f'{color(["bold","green"])}Youtube {color(["underlined","italic"])}Video/Audio{color(["reset","bold","green"])} Downloader by {color(["white","italic"])}Alham_{color(["red"])}\U0000270C{color(["reset"])}')

    link = str(input(
        f'enter url {color(["italic"])}(enter to copy from clipboard){color(["reset"])}: '))

    if link == '':
        link = clipboard.paste()

    utube = YTube(link)

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
        sys.exit()

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
        output = check_output(['ping', '-c', '1', 'google.com'])
        return True
    except CalledProcessError:
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
        print('invalid stream number')
    except Exception as e:
        print(f'{color(["red"])}an error occurred!{color(["reset"])}')
        print(e)
else:
    print('you don\'t have an active internet connection')
