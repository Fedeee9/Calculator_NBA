#! /usr/bin/env python

#Federico Dal Monte
#Calcolatore punteggi Fanta NBA

import openpyxl
import pandas as pd 
import requests
import bs4 as BeautifulSoup


path_excel = r'Formazioni.xlsx'
path_1 = r'ResultTeam1.txt'
path_2 = r'ResultTeam2.txt'

def settings(numD):

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': '*/*',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://fantastatistichenba.it',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://fantastatistichenba.it/statistiche-giocatori-nba/?mode=dunkest&stats=avg&matchdays=all&rounds=all&teams=all&positions=all&player=&crMin=4&crMax=30&param=pdk&order=desc',
        'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
    }
    
    data = {
      'mode'     : 'dunkest',
      'stats'    : 'avg',
      'param'    : 'pdk',
      'order'    : 'desc',
      'matchdays': numD,
      'rounds'   : '1 2'
    }
    
    r = requests.post('https://fantastatistichenba.it/statistiche-giocatori-nba/getStats.php',
        headers=headers, data=data)
        
    return r
    

def read_file(team, path_excel):
    file_excel = openpyxl.load_workbook(path_excel)
    sheet = file_excel.get_sheet_by_name('Formazioni')
    
    name = []
    
    if team == 1:
        for i in range(2,14):
            nome = sheet['A'+str(i)].value
            name.append(nome)
    elif team == 2:
        for i in range(2,14):
            nome = sheet['D'+str(i)].value
            name.append(nome)
    
    return name


    
def calcolaNum(n, name):
    count = 0

    for i in name:
        if i == n:
            return count
        count += 1
    

def calcolo(name, val, team, path_excel, path_1, path_2):
    listPlayer = read_file(team, path_excel)
    
    stringa = ''
    count = 0
    totale = 0
    
    for n in listPlayer:
        count += 1
        if (n in name):
            numero = calcolaNum(n, name)

            if count < 7:
                if count == 1:
                    mol = float(val[numero])
                    cap = mol * 2
                    stringa += "Capitano: "+n+"\n"+str(cap)+"\n"
                    totale += cap
                else:
                    tit = float(val[numero])
                    stringa += "Titolare: "+n+"\n"+str(tit)+"\n"
                    totale += tit
            else:
                div = float(val[numero])
                panc = div / 2
                stringa += "Panchinaro: "+n+"\n"+str(panc)+"\n"
                totale += panc
                
    stringa += "\n\n"
    stringa += "Totale: "+str(totale)
  
    if team == 1:
        print("Team1 Complete")
        file_w = open(path_1, 'w')
        file_w.write(stringa)
    elif team == 2:
        print("Team2 Complete")
        file_w = open(path_2, 'w')
        file_w.write(stringa)

def dati(r, team, path_excel, path_1, path_2):
    soup = BeautifulSoup.BeautifulSoup(r.text,features='lxml')
    t = soup.findAll('a')

    name = []
    val = []

    for n in t:
        string = n.text
        if len(string) > 5:
            name.append(string)
        else:
            if len(string) != 3:
                val.append(string)
                
    punteggio = calcolo(name, val, team, path_excel, path_1, path_2)
    
if __name__ == '__main__':
    print("\n--- Hello guys, this is for you! ---\n")
    days = input('Enter the number of the matchday: ')
    r = settings(days)
    dati(r, 1, path_excel, path_1, path_2)
    dati(r, 2, path_excel, path_1, path_2)
    print("\nGo to see the scores in files ResultTeam1.txt and ResultTeam2.txt")
