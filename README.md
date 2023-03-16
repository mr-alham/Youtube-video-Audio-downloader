# YouTube Video/Audio Downloader
This Python script allows you to download videos and audios from YouTube by simply entering the URL of the video. It uses the PyTube library to download the desired format of the video or audio. The script has a colorful terminal output.

## Prerequisites
* Before running this script, you will need to install PyTube by running the following command:

```python
pip install pytube
```
```python
pip install clipboard
```
![Alt example screenshot of pip installation.](https://i.imgur.com/1goz1jT.png?raw=true "pip installation")

## How to use
* To use this script, simply run the following command:
```python
python youtube_downloader.py
```
##### YouTube video downloading demonstration
![Alt demo screenshot of YouTube video downloading using this script.](https://i.imgur.com/nBeRhx6.png?raw=true "demo of YouTube video downloader")
##### YouTube audio downloading demonstration
![Alt example screenshot of YouTube video downloading using this script.](https://i.imgur.com/obl0vSC.png?raw=true "demo of YouTube audio downloader")

### Brief description
You will be prompted to enter the URL of the video you wish to download. You can also copy the URL to the clipboard and simply hit enter to automatically paste it.

After entering the URL, you will be prompted to select the format you wish to download. You can choose either video or audio. If you enter an incorrect option, you will be prompted again.

If you select video, you will then be prompted to select the video resolution you wish to download. You can choose from 144p, 240p, 360p, 480p, 720p, and 1080p. You can also hit enter to automatically choose the default resolution (360p).

The video or audio will then be downloaded to your default download directory.

Note that an internet connection is required to run this script. If you do not have an internet connection, the script will not run.
### Author

This script was developed by Alham as a personal project. Feel free to use and modify the script as you wish. If you have any questions or suggestions, you can contact me at 
* [alham@duck.com.](mailto:alham@duck.com)
* [twitter](https://twitter.com/alham__aa)
