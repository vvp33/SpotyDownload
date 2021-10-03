from __future__ import unicode_literals
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy
import youtube_dl
from youtubesearchpython import VideosSearch
from urllib.parse import urlparse


client_id = ""
secret = ""
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)


def download(videoresult, ydl_opts):
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([videoresult])

def music(result):
	performers = ""
	music = result['name']
	for names in result["artists"]:
		performers = performers + names["name"] + ", "
	performers = performers.rstrip(", ")
	video = search(music, performers)
	name = f"{performers} - {music}"
	print(name)
	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192',
		}],
		'outtmpl': f'./{name}.webm'
	}
	download(video, ydl_opts)
	print("Готово!")

def search(music, performers):
	videosSearch = VideosSearch(f'{performers} - {music}', limit = 1)
	videoresult = videosSearch.result()["result"][0]["link"]
	return videoresult
# ----------------------------



# -----------Playlist------------
def music1(result):
	tr = []

	for music in result['tracks']["items"]:
		track = music["track"]["name"]
		artists = ""
		for artist in music["track"]["artists"]:
			artists = artists + artist["name"] + ", "
		artists = artists.rstrip(", ")
		ins = {"track": track, "artists": artists}
		tr.append(ins)

	for music in tr:
		video = search(music["track"], music["artists"])
		name = f'{music["artists"]} - {music["track"]}'
		print(name)
		ydl_opts = {
			'format': 'bestaudio/best',
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}],
			'outtmpl': f'./{name}.webm'
		}
		download(video, ydl_opts)
	print("Готово!")


def music2(result):
	tr = []

	for music in result['tracks']["items"]:
		track = music["name"]
		artists = ""
		for artist in music["artists"]:
			artists = artists + artist["name"] + ", "
		artists = artists.rstrip(", ")
		ins = {"track": track, "artists": artists}
		tr.append(ins)

	for music in tr:
		video = search(music["track"], music["artists"])
		name = f'{music["artists"]} - {music["track"]}'
		print(name)
		ydl_opts = {
			'format': 'bestaudio/best',
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}],
			'outtmpl': f'./{name}.webm'
		}
		download(video, ydl_opts)
	print("Готово!")



while True:
	url = input("Введите ссылку на трек/плейлист/альбом или exit для выхода: ")
	if url == "exit":
		break
	types = urlparse(url).path.split("/")[1]
	if types == "track":
		result = spotify.track(url)
		music(result)
	elif types == "playlist":
		result = spotify.playlist(url)
		music1(result)
	elif types == "album":
		result = spotify.album(url)
		music2(result)
	else:
		print("Введите корректную ссылку на трек/плейлист/альбом в Spotify!")
