from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import json
import re
import time

class PsicologoScraper:
    def __init__(self, service_path='Analise-PsyMeet/drivers/chromedriver', url='https://www.psymeetsocial.com/busca', quantidade_de_buscas=500, localidade_por_ddd=''):
        self.service = Service(service_path)
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.get(url)
        self.driver.maximize_window()
        self.quantidade_de_buscas = quantidade_de_buscas
        self.psicologos = {'psicologos': []}
        self.localidade_por_ddd = localidade_por_ddd
        self.wait = WebDriverWait(self.driver, 10)

    def extrair_numero_de_telefone(self, texto):
        regex = r'(\(?\d{2}\)?\s)?(\d{4,5}-\d{4})'
        telefone = ''
        lista = re.findall(regex, texto)
        for numero in lista:
            telefone += numero[0] + numero[1]
        return telefone
    
    def obter_sexo(self, elemento):
        nomeclatura = elemento.find_element(by='class name', value='PsychologistCard_genderName__WCR4n').text
        if nomeclatura == 'Psicóloga':
            return 'F'
        return 'M'
    
        
    #o parametro elemento é um objeto do selenium
    def obter_lista_de_especialidades(self, elemento):
        lista_de_especialidades = []
        especialidades = elemento.find_elements(by='class name', value='PsychologistCard_background__fIIBV')
        for especialidade in especialidades:
            lista_de_especialidades.append(especialidade.text)
        return lista_de_especialidades
    
    def salvar_em_json(self):
        with open('psicologos.json', 'w') as file:
            json.dump(self.psicologos, file, indent=4)

    def scrape(self):
        self.driver.execute_script('window.scrollBy(0, 100)')
        time.sleep(2)
        while self.quantidade_de_buscas > 0:
            lista_psicologo = self.driver.execute_script('return document.getElementsByClassName("PsychologistCard_cardContainer__RKgDL layout_container__1KHHo")')
            try:
                for psicologo in lista_psicologo:
                    numero_telefone = psicologo.find_element(by='class name', value='WhatsappContactButton_phoneNumber__EJ2bP')   
                    ddd = numero_telefone.text.split(' ')[1][1:3]
                    if ddd == self.localidade_por_ddd or self.localidade_por_ddd == '':
                        
                        profissional = {
                            'nome': psicologo.find_element(by='class name', value='PsychologistCard_name__1begB').text,
                            'telefone': self.extrair_numero_de_telefone(numero_telefone.text),
                            'link': psicologo.find_element(by='class name', value='PsychologistCard_profileImageContainer__3iDMG').get_attribute('href'),
                            'especialidades': self.obter_lista_de_especialidades(psicologo),
                            'sexo': self.obter_sexo(psicologo)
                        }
                        self.psicologos['psicologos'].append(profissional)
                    psicologo.parent.execute_script('return arguments[0].remove()', psicologo)
                
                self.driver.find_element(by='class name', value='SeeMoreProfilesButton_seeMoreProfilesButton__1FHZ-').click()
                self.quantidade_de_buscas -= 1

            except:
                print('Erro')
                break

        self.salvar_em_json()

