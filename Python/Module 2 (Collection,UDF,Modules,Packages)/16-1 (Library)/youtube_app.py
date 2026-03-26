from pytubefix import YouTube

url = 'https://www.youtube.com/watch?v=zxlR20V4NFQ&list=RDzxlR20V4NFQ&start_radio=1'

YouTube(url).streams.first().download()