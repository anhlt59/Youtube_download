import os
from tkinter import *
from tkinter import ttk
from pytube import YouTube
from bs4 import BeautifulSoup
import requests

home = os.path.expanduser("~")
file_path = os.path.join(home, "Downloads/")
print(file_path)


def getPlaylistLinks(playlist_url):
    sourceCode = requests.get(playlist_url).text
    soup = BeautifulSoup(sourceCode, 'html.parser')
    folder = soup.find_all('h1')[-1].text.strip()
    domain = 'https://www.youtube.com'
    print(folder)
    # Make a folder to hold all of videos in the playlist if the folder doesn't exist
    try:
        os.mkdir(file_path + folder)
        print('Folder just created')
    except Exception as e:
        print(e)
        pass
    for link in soup.find_all("a", {"dir": "ltr"}):
        href = link.get('href')
        if href.startswith('/watch?'):
            print("Downloading " + link.string.strip() + "\n" +
                  "..............")
            video_url = domain + href
            YouTube(video_url).streams.first().download(file_path + folder)
    return "Download Finished"


def SingleVideoDownload(video_url):
    YouTube(video_url).streams.first().download(file_path)
    return "Download Finished"


def ListVideoDownload(playlist_url):
    return getPlaylistLinks(playlist_url)


def download(*args):
    try:
        if video_link.get() == "" and list_video_link.get() == "":
            result.set("You have not pass a video link")
        elif video_link.get() != "" and list_video_link.get() == "":
            print(video_link.get())
            result.set(SingleVideoDownload(video_link.get()))
        elif video_link.get() == "" and list_video_link.get() != "":
            result.set(ListVideoDownload(list_video_link.get()))
        elif video_link.get() != "" and list_video_link.get() != "":
            result.set('You should just download one video type, not combine video hay videos playlist')
    except Exception as e:
        result.set("Cannot download from this video link")
        # result.set(e)


root = Tk()
root.title("Youtube download videos Toolkit")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

video_link = StringVar()
list_video_link = StringVar()
result = StringVar()

video_url = ttk.Entry(mainframe, width=80, textvariable=video_link)
video_url.grid(column=2, row=1, sticky=(W, E))

list_video_url = ttk.Entry(mainframe, width=80, textvariable=list_video_link)
list_video_url.grid(column=2, row=2, sticky=(W, E))

ttk.Label(mainframe, textvariable=result).grid(column=2, row=3, sticky=(W, E))
ttk.Button(mainframe, text="Download", command=download).grid(column=3, row=3, sticky=W)  # noqa

ttk.Label(mainframe, text="Video").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="PlayList Videos").grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, text="Result: ").grid(column=1, row=3, sticky=E)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

video_url.focus()
root.bind('<Return>', download)

root.mainloop()
