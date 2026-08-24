# -*- coding: utf-8 -*-
"""
Gera coordenadas_aerodromos.json a partir da base OurAirports.

Rode UMA VEZ na sua máquina (não no servidor) e versione o JSON no repositório:

    python gerar_coordenadas.py

Assim o app deixa de depender de internet no momento do cálculo, e a coordenada
usada em cada cotação fica auditável no histórico do Git.
Repita sempre que incluir novos aeródromos em dados.py.
"""

import csv
import json
import sys
import urllib.request

from dados import AEROPORTOS, COORDS_BACKUP

URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"
SAIDA = "coordenadas_aerodromos.json"


def main():
    print(f"Baixando {URL} ...")
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "DTA-Planner/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            linhas = [linha.decode("utf-8") for linha in resp.readlines()]
    except Exception as e:
        print(f"ERRO: falha no download ({e}).")
        return 1

    coords = {}
    for linha in csv.DictReader(linhas):
        if linha["ident"] in AEROPORTOS:
            coords[linha["ident"]] = {
                "lat": round(float(linha["latitude_deg"]), 6),
                "lon": round(float(linha["longitude_deg"]), 6),
            }

    # completa o que a base pública não tiver com o backup embutido
    for icao, c in COORDS_BACKUP.items():
        coords.setdefault(icao, c)

    faltantes = sorted(icao for icao in AEROPORTOS if icao not in coords)

    with open(SAIDA, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(coords.items())), f, ensure_ascii=False, indent=2)

    print(f"OK: {len(coords)} de {len(AEROPORTOS)} aeródromos gravados em {SAIDA}.")
    if faltantes:
        print("ATENÇÃO — sem coordenada, preencha manualmente em dados.COORDS_BACKUP:")
        for icao in faltantes:
            print(f"  {icao} - {AEROPORTOS[icao]['cidade']}/{AEROPORTOS[icao]['uf']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
