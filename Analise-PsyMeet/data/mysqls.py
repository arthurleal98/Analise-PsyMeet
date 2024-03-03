import mysql.connector
import json

class BancoDeDados:
    def __init__(self, host='localhost', user='root', password='root'):
        self.con = mysql.connector.connect(host=host, user=user, password=password)
        self.cursor = self.con.cursor()
        self.cursor.execute('create database if not exists psicologos')
        self.cursor.execute('use psicologos')
        self.cursor.execute('create table if not exists psicologos (id int primary key auto_increment, nome varchar(100), telefone varchar(15) unique, link varchar(200), sexo char(1))')
        self.cursor.execute('create table if not exists especialidades (especialidade varchar(100), id_psicologo int, foreign key(id_psicologo) references psicologos(id))')
        self.cursor.execute('commit')

    def transformar_json_em_sql(self):
        with open('data/psicologos.json', 'r') as file:
            psicologos = json.load(file)
            for psicologo in psicologos['psicologos']:
                # Inserindo dados na tabela psicologos
                self.cursor.execute(f'insert into psicologos (nome, telefone, link, sexo) values ("{psicologo["nome"]}", "{psicologo["telefone"]}", "{psicologo["link"]}", "{psicologo["sexo"]}")')
                self.con.commit()  # Realiza o commit após cada inserção na tabela psicologos
                id_psicologo = self.cursor.lastrowid
                
                # Inserindo dados na tabela especialidades
                for especialidade in psicologo['especialidades']:
                    self.cursor.execute(f'insert into especialidades (especialidade, id_psicologo) values ("{especialidade}", {id_psicologo})')
                    self.con.commit()  # Realiza o commit após cada inserção na tabela especialidades
        
        self.cursor.close()
        self.con.close()
    
    def retornar_dados(self, tabela):
        self.cursor.execute(f'select * from {tabela}')
        return self.cursor.fetchall()

    def retornar_nomes_colunas(self, tabela):
        self.cursor.execute(f'show columns from {tabela}')
        return self.cursor.fetchall()
    
    
# Executa o método transformar_json_em_sql

