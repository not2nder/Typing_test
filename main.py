import time
import datetime as dt
import os

import requests
import json

from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.columns import Columns

import keyboard

from pick import pick

import webbrowser

console = Console()

terminal_size = (os.get_terminal_size().columns)-1

def request_words(qtd:int, lan:str) -> str:
    url = f"https://word-generator-api.not2nder1.repl.co/{qtd}-{lan}"
    return str(" ".join(requests.get(url).json()))

def get_latest_date():
    return f"{dt.datetime.now().strftime('%X')[0:5]} {dt.datetime.now().strftime('%x')}"

def voltar():
    print(f"[bold red](X) - [bold white]Voltar")
    while True:
        if keyboard.is_pressed('x'):
            keyboard.press('backspace')
            menu()
            break

def test(qtd:int,lan:str) -> dict:
    words = request_words(qtd,lan)
    print(Panel.fit(f"\n{words}\n",title="[i][b]Comece a Escrever:",width=terminal_size))
    st = time.time()
    u_input = input(": ")
    end = time.time()
    elapsed = end-st

    if len(words) > len(u_input):
        certas = int(len([i for i in range(len(u_input)) if u_input[i] == words[i]]))
    else:
        certas = int(len([i for i in range(len(words)) if words[i] == u_input[i]]))

    return {
        "qtd":qtd,
        "lan":lan,
        "elapsed":elapsed,
        "words":words,
        "input":u_input,
        "wps":certas//elapsed,
        "acc":(certas/len(words))*100,
        "err":((len(words)-certas)/len(words))*100
    }

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

def set_history(results:dict):
    all_data = []
    try:
        with open("data\data.json","r") as file:
            all_data = json.load(file)
    except:
        pass
    all_data.append(results) 
    with open("data\data.json","w") as file:
        json.dump(all_data,file,indent=4)
        
def get_results(results:dict):
    results["date"] = get_latest_date()
    set_history(results)
    table = Panel.fit(
        f"{results['words']}\n \n{check_words(results['words'],results['input'])}",
        title="[b][i]Words",
        padding=(1,2),
        )
    
    res = f"\n[b]Elapsed: [cyan]{results['elapsed']:.2f}s[/cyan] \nWPS: [cyan]{results['wps']:.2F}[/cyan] \nACC: [green]{results['acc']:.2f}%[/green] \nERR: [red]{results['err']:.2f}%[/red][/b]"
    console.print(Panel.fit(Columns([table,res]),
                            title=F"[b i]Resultados - {results['lan']}({results['qtd']})",
                            padding=(1,2),
                            width=55),
                            )
    voltar()

    
def escolha(list:list, title:str,indicador:str):
    option, index = pick(list,title,indicator=indicador)
    return option

def github():
    webbrowser.open("www.github.com/not2nder")
    time.sleep(0.3)
    menu()

def api():
    webbrowser.open("https://word-generator-api.not2nder1.repl.co/10-en")
    time.sleep(0.3)
    menu()

def menu():
    os.system('cls')
    title = "Typing Test"
    options = ["Teste","Histórico","API","Github","Sair"]
    op = escolha(options,title,'•')

    commands = {
        "Teste":select_test,
        "API": api,
        "Github": github,
        "Histórico":see_his,
        "Sair":exit
    }
    if op in commands:
        func = commands[op]
        func()

def typerace(qtd,lan):
    race = test(qtd,lan)
    time.sleep(1)
    os.system('cls')
    get_results(race)

def select_test():
    os.system('cls')
    title = "ESCOLHA SEU IDIOMA"
    options = ["EN","PT"]
    idioma = escolha(options,title,'•')
    quant = escolha([10,20,30,50,100],"Quantidade",'•')
    typerace(int(quant),str(idioma).lower())
    
def see_his():
    os.system('cls')
    time.sleep(0.6)
    print(f"[b][i]{'HISTÓRICO'.center(50)}")
    time.sleep(1)
    with open("data\data.json","r") as file:
        content = json.load(file)
        for data in content:
            panel = Panel(f"Teste: [bold]{data['words']}[/bold]\n \nRecebido: {check_words(data['words'],data['input'])} \n\nTempo: {float(data['elapsed']):.2f}\nPPS: {data['wps']}\nPrecisão: {float(data['acc']):.2f}\nTaxa de Erro: {data['err']}"
                          ,title=f"[i]{data['date']} - {data['lan']}({data['qtd']})",
                          padding=(1,2),
                          width=50)
            console.print(panel)
    voltar()

menu()