
# pip install beautifulsoup4
# pip install requests
# pip install lxml
# pip install prettytable
# pip install asyncio
# pip install fake-useragent

import requests
from bs4 import BeautifulSoup
import requests
import xml.etree.ElementTree as ET


class Parser_valut:
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36', 'accept': '*/*'
    }

    def __init__(self, URL):
        self.URL = URL
        
    def DRUM_bank(self, headers=headers):  # отклик
        data_min_max_bank = {}
        try:
            drum = {}
            min_max = {}
            resp = requests.get(self.URL, headers)  # пробуем подключиться
            soup = BeautifulSoup(resp.text, 'lxml')
            table_all = soup.find("div", class_ ="w-full overflow-auto -mt-40 pt-40")
            name_banks = table_all.find("div", class_="w-full grow rounded-tl-xl").find_all("img")
            curs = table_all.find_all("div", class_="flex h-12 md:h-10 bg-white group border-b border-b-N40")
            # Сортируем от min до max значения 
            name_bank = []
            for i in name_banks:
                name_bank.append(i.get("alt").strip())
           
            i = 0   
            for n in curs:
                cena_pokupka = n.find_all("div")[-6].text.strip()
                cena_prodaga = n.find_all("div")[-1].text.strip()
                data_min_max_bank[name_bank[i]] = cena_pokupka
                print(' {} {:>3} {:>12}'.format(name_bank[i].ljust(25, '.'),
                    cena_pokupka , cena_prodaga)) # отступы
                drum[name_bank[i]]=(cena_pokupka, cena_prodaga)
                            
                i += 1
                
            # Сортируем от min до max значения 
            sorted_values = sorted(data_min_max_bank.values(), reverse=True) 
            # Sort the values
            maximum_dr = max(sorted_values)
            minimum_dr = min(sorted_values)
            min_max['max'] = maximum_dr        
            min_max['min'] = minimum_dr
            
            print("  ")
            print("-- Банки: ----------------------------------")
            print(f" Максимум: {maximum_dr} руб.")
            print(f" Минимум:  {minimum_dr} руб.")
            """
            print("--------------------------------------------")
            print(" При цене: 150 000 драм")
            arenda = 150000/float(maximum_dr)
            print(f" Аренда квартиры: {math.ceil(arenda)} руб.")
            arenda = 150000/float(minimum_dr)
            print(f" Аренда квартиры: {math.ceil(arenda)} руб.")
            print("--------------------------------------------")
            """
            # return drum, min_max
            return minimum_dr, maximum_dr, drum
        except:
            return 0
    
    
    def DRUM_obmennik(self, headers=headers):  # отклик
        data_min_max_bank = {}
        try:
            drum = {}
            min_max = {}
            resp = requests.get(self.URL, headers)  # пробуем подключиться
            soup = BeautifulSoup(resp.text, 'lxml')
            table_all = soup.find("div", class_ ="w-full overflow-auto -mt-40 pt-40")
            name_banks = table_all.find("div", class_="w-full grow rounded-tl-xl").find_all("img")
            curs = table_all.find_all("div", class_="flex h-12 md:h-10 bg-white group border-b border-b-N40")
            # Сортируем от min до max значения 
            name_bank = []
            for i in name_banks:
                name_bank.append(i.get("alt").strip())
           
            i = 0   
            for n in curs:
                cena_pokupka = n.find_all("div")[-6].text.strip()
                cena_prodaga = n.find_all("div")[-1].text.strip()
                data_min_max_bank[name_bank[i]] = cena_pokupka
                # print('{} {:>3} {:>12}'.format(name_bank[i].ljust(25, '.'),
                #     cena_pokupka , cena_prodaga)) # отступы
                drum[name_bank[i]]=(cena_pokupka, cena_prodaga)
                i += 1
                
            sorted_values = sorted(data_min_max_bank.values(), reverse=True) 
            
            # Sort the values
            maximum_dr = max(sorted_values)
            minimum_dr = min(sorted_values)
            min_max['max'] = maximum_dr                 
            min_max['min'] = minimum_dr          
            
            print("-- Обменник: ------------------------------")      
            print(f" Максимум: {maximum_dr} руб.")
            print(f" Минимум:  {minimum_dr} руб.")
            print("-------------------------------------------")
            # return drum, min_max
            return minimum_dr, maximum_dr, drum
        except:
            return 0
    
    
    def USD_EUR_parse(self, headers=headers):  # отклик
        try:
            resp = requests.get(self.URL, headers)  # пробуем подключиться
            soup = BeautifulSoup(resp.text, 'lxml')
            exit_USD = soup.find("table", class_="default-table").find("tbody").find("tr", class_="row body odd")
            exit_EUR = soup.find("table", class_="default-table").find("tbody").find("tr", class_="row body even")
            usd = exit_USD.find_all("td")[1].text.strip()
            eur = exit_EUR.find_all("td")[1].text.strip()
            return usd, eur
        except:
            return 0
        
    def get_html(self):
        try:
            page = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
            with open("cbr.xml", "wb") as f:
                f.write(page.content)
            return page.content
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения/скачивания с сайта!')
            return False     

    def CB_Bank(self):
      self.get_html()
        
      # Парсим XML файл
      tree = ET.parse("cbr.xml")
      root = tree.getroot()
      
      # Получаем дату и имя рынка
      date = root.attrib.get('Date')
      # market_name = root.attrib.get('name')
      # print(f"Имя рынка: {market_name}\n")
      
      print(f"-- ЦБ РФ {date}: ----------------------") 
      # Обходим каждый элемент Valute
      for valute in root.findall('Valute'):
          # Получаем атрибуты валюты
          valute_id = valute.attrib.get('ID')
          
          # Получаем значения элементов валюты
          # num_code = valute.find('NumCode').text
          # char_code = valute.find('CharCode').text
          # nominal = valute.find('Nominal').text
          VunitRate = valute.find('VunitRate').text
          name = valute.find('Name').text
          value = valute.find('Value').text
          
          # Drum
          if valute_id == "R01060":
            dr = VunitRate
            dr_str = dr.replace(",", ".")
            calc = float(dr_str)
            
            # Рассчитываем % от числа
            percentage = calc * 0.02 # 2.32/100%
            result = calc + percentage
            calc_round = round(1/float(result), 2)
            
            #result = calc + percentage
            print(f" Наш банкомат (расчётное): {calc_round} ({round(result, 6)})\n\n")
            
            #print(f" {name}: {calc} руб.") # курс ЦБ на сайте
          
          # Выводим информацию о валюте
          
          if valute_id == "R01235" or valute_id == "R01239":
            print(f" {name}: {value} руб.")
        
        
        
        
# if __name__ == "__main__": 
    # # USD, EUR = Parser_valut("https://myfin.by/currency/cb-rf").USD_EUR_parse()
    # # print(" ")
    # # print("--------------------------------------------")
    # # print(f" Доллар: {USD} руб.")
    # # print(f" Евро:   {EUR} руб.")
    # print(" ")
    # print("www.rate.am")
    # print("--------------------------------------------")
    
    # DRM = Parser_valut("https://www.rate.am/ru/armenian-dram-exchange-rates/banks").DRUM_bank()
    # DRM_OBM = Parser_valut("https://www.rate.am/ru/armenian-dram-exchange-rates/exchange-points").DRUM_obmennik()
    
    # print(" ")
    # """
    # print("--------------------------------------------")
    # print(" При цене: 150 000 драм")
    # arenda = 150000/float(int(DRM[0][0]))
    # print(f" Аренда квартиры: {math.ceil(arenda)} руб.")
    # arenda = 150000/float(int(DRM[1][0]))
    # print(f" Аренда квартиры: {math.ceil(arenda)} руб.")
    # print("--------------------------------------------")
    #  """       
    # Parser_valut("bank").CB_Bank()
    # print("--------------------------------------------")
    
    

