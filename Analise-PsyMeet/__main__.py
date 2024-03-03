#importar mysql.py
import sys
from data.mysqls import BancoDeDados

print(BancoDeDados().retornar_dados('especialidades'))


