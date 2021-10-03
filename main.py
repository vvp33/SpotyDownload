from __future__ import unicode_literals
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from youtubesearchpython import VideosSearch
import youtube_dl

url = input("Введи ссылку на трек: ")
client_id = "" # Сюда вводим полученные данные из панели спотифая
secret = "" # Сюда вводим полученные данные из панели спотифая

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)

def music(result):
  performers = ""
  music = result['name']
  for names in result["artists"]:
    performers = performers + names["name"] + ", "
  performers = performers.rstrip(", ")
  video = search(music, performers)
  name = f"{performers} - {music}"
  ydl_opts = {'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192',}], 'outtmpl': f'./{name}.webm'}
  download(video, ydl_opts)

def search(music, performers):
  videosSearch = VideosSearch(f'{performers} - {music}', limit = 1)
  videoresult = videosSearch.result()["result"][0]["link"]
  return videoresult

def download(videoresult, ydl_opts):
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([videoresult])

result = spotify.track(url)
music(result)
