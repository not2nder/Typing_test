import requests
import os
from dotenv import load_dotenv

from rich import print
from rich.panel import Panel
from rich.console import Console

console = Console()

load_dotenv()
api_key = os.getenv("API_KEY")

def get_lyrics(api_key, song_name, artist_name):
    base_url = "https://api.musixmatch.com/ws/1.1/matcher.lyrics.get"
    params = {
        "apikey": api_key,
        "q_track": song_name,
        "q_artist": artist_name
    }
    data = requests.get(base_url, params=params).json()
    
    if data["message"]["header"]["status_code"] == 200:
        lyrics = data["message"]["body"]["lyrics"]["lyrics_body"].split('\n')
        return '\n'.join(lyrics[0:len(lyrics)-5])
    else:
        return f"Erro de Requisição, Tente novamente"

os.system('cls')

lyrics = get_lyrics(api_key,"pastel ghost","dark beach")

song_lines = [line for line in lyrics.split("\n") if line != ""]

novas = []

def check_words(word: str, input_str: str) -> str:
    new_string = ""
    min_length = min(len(word), len(input_str))

    for i in range(min_length):
        if word[i] == input_str[i]:
            new_string += f"[bold green]{input_str[i]}[/bold green]"
        elif word[i] == " " and input_str[i] != " ":
            new_string += f"[bold grey7]{input_str[i]}[/bold grey7]"
        else:
            new_string += f"[bold red]{input_str[i]}[/bold red]"

    if len(word) > len(input_str):
        new_string += f"[bold red]{word[min_length:]}[/bold red]"
    else:
        new_string += f"[bold grey7]{input_str[min_length:]}[/bold grey7]"
        
    return new_string

teste = [
    'laying on a dark beach',
    'pulsing waves cover me',
    'flowers bloom on the sea',
    'silver sand underneath',
    'talk to me as i am sleeping',
    "hold me while i'm dreaming"
]
song = [
    'Laying on a dark beach',
    'Pulsing waves cover me',
    'Flowers bloom on the sea',
    'Silver sand underneath',
    'Talk to me as I am sleeping',
    "Hold me while I'm dreaming"
]

words = '\n'.join([check_words(teste[i],song[i]) for i in range(len(teste))])
print(Panel(words,title="Results",padding=(2,2),width=50))