import pandas as pd
from bs4 import BeautifulSoup
import requests as rq
import time
import calendar
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--fechas',
                help='LISTA DE FECHAS' +
                'SEPARA POR UNA COMA',
                action="store", required=True)
args = parser.parse_args()
args2 = args.fechas
fechas = [str(item) for item in args2.split(',')]

def ScrappingPTE(fechas):
  l = []

  for fecha in fechas:
    print(fecha)
    baseURL = 'http://visitas.promperu.gob.pe/controlVisitas/index.php?r=consultas%2FvisitaConsulta%2FupdateVisitasConsultaResultGrid&ajax=lst-visitas-consulta-result-grid&VisitaConsultaQueryForm[feConsulta]=13/03/2020'
    res = rq.post(baseURL,data={'VisitaConsultaQueryForm[feConsulta]':fecha})
    soup = BeautifulSoup(res.content)
    table = soup.find('table', {'class': 'items'})
    rows = table.find_all('tr')
    rows2 = rows[1:len(rows)]
    for tr in rows2:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        l.append(row)
  data = pd.DataFrame(l, columns=["FECHA",	"VISITANTE",	"DOCUMENTO",	"ENTIDAD",	"MOTIVO",	"EMPLEADO", "PUBLICO",	"OFICINA / CARGO","LUGAR DE REUNION"	"HORA ING.","HORA SAL."])
  ts = calendar.timegm(time.gmtime())
  data.to_excel("DATA_"+str(ts)+".xlsx",sheet_name='Data_PTE')  

if __name__ == "__main__":
    ScrappingPTE(fechas)