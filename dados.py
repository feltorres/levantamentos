# -*- coding: utf-8 -*-
"""
Base de dados estática do Planejador de Missões Aéreas - DTA.

Este módulo NÃO importa Streamlit de propósito: assim ele pode ser usado por
scripts auxiliares (gerar_coordenadas.py) e pela suíte de testes sem subir a
interface web.

FONTE DOS DADOS DE PISTA/BALIZAMENTO: preencher abaixo.
DATA DA ÚLTIMA CONFERÊNCIA: preencher abaixo.
"""

FONTE_DADOS_AERODROMOS = "PREENCHER (ex.: ROTAER / AIP-Brasil / planilha interna DTA)"
DATA_ULTIMA_CONFERENCIA = "PREENCHER (ex.: 2026-08-18)"

# ---------------------------------------------------------------------------
# AERÓDROMOS
# ---------------------------------------------------------------------------
# Campos:
#   cidade         -> nome do município (usado na tabela final)
#   uf             -> unidade federativa
#   pista          -> "COMPRIMENTO x LARGURA" em metros, ou texto de situação
#   op_noturna     -> Sim | Não | Inoperante | Sim. Só decola.
#   restricao_anac -> (opcional) True se houver embargo do órgão regulador
# ---------------------------------------------------------------------------
AEROPORTOS = {
    # --- Minas Gerais e Região ---
    "SBBH": {"cidade": "Belo Horizonte", "pista": "2364 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SBCF": {"cidade": "Confins", "pista": "3600 x 45", "op_noturna": "Sim", "uf": "MG"},
    "SNLI": {"cidade": "Abaeté", "pista": "1200 x 30", "op_noturna": "Não", "uf": "MG", "restricao_anac": True},
    "SNFE": {"cidade": "Alfenas", "pista": "1600 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNAR": {"cidade": "Almenara", "pista": "1400 x 30", "op_noturna": "Inoperante", "uf": "MG"},
    "SNUI": {"cidade": "Araçuaí", "pista": "1200 x 30", "op_noturna": "Não", "uf": "MG", "restricao_anac": True},
    "SNAG": {"cidade": "Araguari", "pista": "1500 x 30", "op_noturna": "Não", "uf": "MG", "restricao_anac": True},
    "SBAX": {"cidade": "Araxá", "pista": "1900 x 30", "op_noturna": "Inoperante", "uf": "MG"},
    "SNBG": {"cidade": "Aimorés", "pista": "1200 x 30", "op_noturna": "Não", "uf": "MG", "restricao_anac": True},
    "SBBQ": {"cidade": "Barbacena", "pista": "1760 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNGQ": {"cidade": "Bom Despacho", "pista": "1000 x 18", "op_noturna": "Sim", "uf": "MG"},
    "SNCA": {"cidade": "Campo Belo", "pista": "1420 x 30", "op_noturna": "Não", "uf": "MG"},
    "SIRS": {"cidade": "Campo Florido", "pista": "1200 x 30", "op_noturna": "Não", "uf": "MG"},
    "SICK": {"cidade": "Capelinha", "pista": "1229 x 30", "op_noturna": "Sim. Só decola.", "uf": "MG"},
    "SNCT": {"cidade": "Caratinga", "pista": "1080 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNEW": {"cidade": "Carneirinho", "pista": "1250 x 29", "op_noturna": "Não", "uf": "MG"},
    "SNXB": {"cidade": "Caxambu", "pista": "1500 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SDNA": {"cidade": "Comendador Gomes", "pista": "1300 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNKD": {"cidade": "Conceição do Mato Dentro", "pista": "960 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNKF": {"cidade": "Conselheiro Lafaiete", "pista": "902 x 24", "op_noturna": "Não", "uf": "MG", "restricao_anac": True},
    "SIWH": {"cidade": "Coromandel", "pista": "1300 x 20", "op_noturna": "Sim", "uf": "MG"},
    "SNQV": {"cidade": "Curvelo", "pista": "1200 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNDT": {"cidade": "Diamantina", "pista": "1700 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNDV": {"cidade": "Divinópolis", "pista": "1520 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNXV": {"cidade": "Felixlândia", "pista": "1500 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNFU": {"cidade": "Frutal", "pista": "1320 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SBZM": {"cidade": "Goianá", "pista": "2525 x 45", "op_noturna": "Sim", "uf": "MG"},
    "SBGV": {"cidade": "Governador Valadares", "pista": "1701 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SSVG": {"cidade": "Guapé", "pista": "1200 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNSR": {"cidade": "Guarda-Mor", "pista": "1100 x 25", "op_noturna": "Não", "uf": "MG"},
    "SNGX": {"cidade": "Guaxupé", "pista": "1500 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SSDK": {"cidade": "Igaratinga", "pista": "1300 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SBIP": {"cidade": "Ipatinga", "pista": "2004 x 45", "op_noturna": "Sim", "uf": "MG"},
    "SNZK": {"cidade": "Itacarambi", "pista": "1560 x 24", "op_noturna": "Não", "uf": "MG"},
    "SNYB": {"cidade": "Ituiutaba", "pista": "1782 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNYU": {"cidade": "Iturama", "pista": "1550 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNLG": {"cidade": "Jaboticatubas", "pista": "1260 x 20", "op_noturna": "Não", "uf": "MG"},
    "SNMK": {"cidade": "Jaíba", "pista": "1531 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNAP": {"cidade": "Janaúba", "pista": "1500 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNJN": {"cidade": "Januária", "pista": "NÃO HOMOLOGADO", "op_noturna": "Não", "uf": "MG", "restricao_anac": True},
    "SNJI": {"cidade": "Jequitaí", "pista": "1080 x 18", "op_noturna": "Não", "uf": "MG"},
    "SNJQ": {"cidade": "Jequitinhonha", "pista": "1130 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNJP": {"cidade": "João Pinheiro", "pista": "1300 x 23", "op_noturna": "Não", "uf": "MG"},
    "SBJF": {"cidade": "Juiz de Fora", "pista": "1535 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNLY": {"cidade": "Lagoa da Prata", "pista": "1000 x 20", "op_noturna": "Não", "uf": "MG"},
    "SBLS": {"cidade": "Lagoa Santa", "pista": "1840 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SSOL": {"cidade": "Lavras", "pista": "1500 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNJM": {"cidade": "Manhuaçu", "pista": "1170 x 30", "op_noturna": "Não", "uf": "MG"},
    "SWWM": {"cidade": "Mantena", "pista": "1050 x 18", "op_noturna": "Não", "uf": "MG"},
    "SSYF": {"cidade": "Monte Alegre de Minas", "pista": "1200 x 24", "op_noturna": "Não", "uf": "MG"},
    "SBMK": {"cidade": "Montes Claros", "pista": "2100 x 45", "op_noturna": "Sim", "uf": "MG"},
    "SNBM": {"cidade": "Muriaé", "pista": "1140 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNNU": {"cidade": "Nanuque", "pista": "1220 x 23", "op_noturna": "Sim", "uf": "MG"},
    "SNTD": {"cidade": "Natalândia", "pista": "1350 x 23", "op_noturna": "Não", "uf": "MG"},
    "SSYD": {"cidade": "Nova Ponte", "pista": "1500 x 45", "op_noturna": "Não", "uf": "MG"},
    "SNRZ": {"cidade": "Oliveira", "pista": "1180 x 18", "op_noturna": "Não", "uf": "MG"},
    "SNOF": {"cidade": "Ouro Fino", "pista": "1050 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNPA": {"cidade": "Pará de Minas", "pista": "1260 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNZR": {"cidade": "Paracatu", "pista": "1500 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SWZT": {"cidade": "Paraopeba", "pista": "1240 x 23", "op_noturna": "Não", "uf": "MG"},
    "SNOS": {"cidade": "Passos", "pista": "1500 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNPD": {"cidade": "Patos de Minas", "pista": "1700 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNPJ": {"cidade": "Patrocínio", "pista": "1200 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNPX": {"cidade": "Pirapora", "pista": "1480 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNUH": {"cidade": "Piumhi", "pista": "1148 x 30", "op_noturna": "Não", "uf": "MG"},
    "SBPC": {"cidade": "Poços de Caldas", "pista": "1515 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNCZ": {"cidade": "Ponte Nova", "pista": "1060 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNZA": {"cidade": "Pouso Alegre", "pista": "1280 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNSS": {"cidade": "Salinas", "pista": "1480 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SIEX": {"cidade": "Santa Vitória", "pista": "1106 x 18", "op_noturna": "Não", "uf": "MG"},
    "SNJV": {"cidade": "São João da Ponte", "pista": "1600 x 18", "op_noturna": "Não", "uf": "MG"},
    "SNJR": {"cidade": "São João Del Rei", "pista": "1400 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SNLO": {"cidade": "São Lourenço", "pista": "1300 x 30", "op_noturna": "Não", "uf": "MG"},
    "SNPY": {"cidade": "São Sebastião do Paraíso", "pista": "1600 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SDJR": {"cidade": "Sete Lagoas", "pista": "1500 x 23", "op_noturna": "Sim", "uf": "MG"},
    "SNTO": {"cidade": "Teófilo Otoni", "pista": "1190 x 23", "op_noturna": "Sim", "uf": "MG"},
    "SNVI": {"cidade": "Três Corações", "pista": "1300 x 23", "op_noturna": "Sim", "uf": "MG"},
    "SNAS": {"cidade": "Três Marias", "pista": "1500 x 45", "op_noturna": "Não", "uf": "MG"},
    "SNFI": {"cidade": "Tupaciguara", "pista": "1500 x 26", "op_noturna": "Não", "uf": "MG"},
    "SNUB": {"cidade": "Ubá", "pista": "1402 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SBUR": {"cidade": "Uberaba", "pista": "1759 x 45", "op_noturna": "Sim", "uf": "MG"},
    "SBUL": {"cidade": "Uberlândia", "pista": "2100 x 45", "op_noturna": "Sim", "uf": "MG"},
    "SNUN": {"cidade": "Unaí", "pista": "1185 x 30", "op_noturna": "Não", "uf": "MG"},
    "SBVG": {"cidade": "Varginha", "pista": "2100 x 30", "op_noturna": "Sim", "uf": "MG"},
    "SSAT": {"cidade": "Vazante", "pista": "1500 x 22", "op_noturna": "Sim", "uf": "MG"},
    "SNVC": {"cidade": "Viçosa", "pista": "1105 x 30", "op_noturna": "Sim", "uf": "MG"},

    # --- Capitais brasileiras ---
    "SBAR": {"cidade": "Aracaju", "pista": "2200 x 45", "op_noturna": "Sim", "uf": "SE"},
    "SBBE": {"cidade": "Belém", "pista": "2800 x 45", "op_noturna": "Sim", "uf": "PA"},
    "SBBV": {"cidade": "Boa Vista", "pista": "2700 x 45", "op_noturna": "Sim", "uf": "RR"},
    "SBBR": {"cidade": "Brasília", "pista": "3300 x 45", "op_noturna": "Sim", "uf": "DF"},
    "SBCG": {"cidade": "Campo Grande", "pista": "2600 x 45", "op_noturna": "Sim", "uf": "MS"},
    "SBCY": {"cidade": "Cuiabá", "pista": "2300 x 45", "op_noturna": "Sim", "uf": "MT"},
    "SBCT": {"cidade": "Curitiba", "pista": "2218 x 45", "op_noturna": "Sim", "uf": "PR"},
    "SBFL": {"cidade": "Florianópolis", "pista": "2400 x 45", "op_noturna": "Sim", "uf": "SC"},
    "SBFZ": {"cidade": "Fortaleza", "pista": "2545 x 45", "op_noturna": "Sim", "uf": "CE"},
    "SBGO": {"cidade": "Goiânia", "pista": "2500 x 45", "op_noturna": "Sim", "uf": "GO"},
    "SBGR": {"cidade": "Guarulhos (SP)", "pista": "3700 x 45", "op_noturna": "Sim", "uf": "SP"},
    "SBJP": {"cidade": "João Pessoa", "pista": "2515 x 45", "op_noturna": "Sim", "uf": "PB"},
    "SBMQ": {"cidade": "Macapá", "pista": "2100 x 45", "op_noturna": "Sim", "uf": "AP"},
    "SBMO": {"cidade": "Maceió", "pista": "2602 x 45", "op_noturna": "Sim", "uf": "AL"},
    "SBEG": {"cidade": "Manaus", "pista": "4000 x 45", "op_noturna": "Sim", "uf": "AM"},
    "SBSG": {"cidade": "Natal", "pista": "3000 x 45", "op_noturna": "Sim", "uf": "RN"},
    "SBPJ": {"cidade": "Palmas", "pista": "2500 x 45", "op_noturna": "Sim", "uf": "TO"},
    "SBPA": {"cidade": "Porto Alegre", "pista": "3200 x 45", "op_noturna": "Sim", "uf": "RS"},
    "SBPV": {"cidade": "Porto Velho", "pista": "2400 x 45", "op_noturna": "Sim", "uf": "RO"},
    "SBRF": {"cidade": "Recife", "pista": "3007 x 45", "op_noturna": "Sim", "uf": "PE"},
    "SBRB": {"cidade": "Rio Branco", "pista": "3558 x 45", "op_noturna": "Sim", "uf": "AC"},
    "SBRJ": {"cidade": "Rio de Janeiro (S. Dumont)", "pista": "1323 x 42", "op_noturna": "Sim", "uf": "RJ"},
    "SBGL": {"cidade": "Rio de Janeiro (Galeão)", "pista": "4000 x 45", "op_noturna": "Sim", "uf": "RJ"},
    "SBSV": {"cidade": "Salvador", "pista": "3003 x 45", "op_noturna": "Sim", "uf": "BA"},
    "SBSL": {"cidade": "São Luís", "pista": "2385 x 45", "op_noturna": "Sim", "uf": "MA"},
    "SBSP": {"cidade": "São Paulo (Congonhas)", "pista": "1940 x 45", "op_noturna": "Sim", "uf": "SP"},
    "SBTE": {"cidade": "Teresina", "pista": "2200 x 45", "op_noturna": "Sim", "uf": "PI"},
    "SBVT": {"cidade": "Vitória", "pista": "2058 x 45", "op_noturna": "Sim", "uf": "ES"},
}

# ---------------------------------------------------------------------------
# FROTA
# ---------------------------------------------------------------------------
# Campos:
#   vel_kt              -> velocidade de cruzeiro em nós (KT / knots)
#   vel_kt_t2           -> velocidade da 2ª tabela (apenas King Air B200)
#   regra_tabela_dupla  -> aplica vel_kt_t2 quando o tempo base >= 1 h
#   valor_hora          -> custo da hora de voo em reais
#   pax                 -> capacidade (texto livre, exibido na tabela)
#   tipo_sigla          -> sigla da coluna ANV na tabela final
#   is_heli             -> asa rotativa (ignora restrição ANAC e pista mínima)
#   requer_pista_1200   -> exige pista de no mínimo 1200 m
# ---------------------------------------------------------------------------
FROTA = {
    "Citation Bravo": {
        "vel_kt": 290, "valor_hora": 18266.14, "pax": "07 Pax",
        "requer_pista_1200": True, "tipo_sigla": "JATO", "is_heli": False,
    },
    "King Air B350 (PR-XAA)": {
        "vel_kt": 220, "valor_hora": 12318.67, "pax": "Até 09 Pax C/ bagagem",
        "tipo_sigla": "B350", "is_heli": False,
    },
    "King Air B300 (PP-EJO)": {
        "vel_kt": 220, "valor_hora": 9705.13, "pax": "7 Pax c/ Bagagem\n9 Pax s/ Bagagem",
        "tipo_sigla": "B300", "is_heli": False,
    },
    "King Air B200 (PTWGS)": {
        "vel_kt": 200,
        "vel_kt_t2": 225,
        "valor_hora": 9705.13,
        "pax": "7 Pax c/ Bagagem\n9 Pax s/ Bagagem",
        "regra_tabela_dupla": True,
        "tipo_sigla": "B200",
        "is_heli": False,
    },
    "King Air C90 (PR/PT-OSO)": {
        "vel_kt": 200, "valor_hora": 6323.05, "pax": "06 Pax",
        "tipo_sigla": "C90", "is_heli": False,
    },
    "Dauphin N3 (PR-DTG)": {
        "vel_kt": 110, "valor_hora": 26135.07, "pax": "06 Pax",
        "tipo_sigla": "DAUPHIN N3", "is_heli": True,
    },
    "Dauphin N2 (PP-EPO)": {
        "vel_kt": 110, "valor_hora": 26135.07, "pax": "05 Pax",
        "tipo_sigla": "DAUPHIN N2", "is_heli": True,
    },
    "Esquilo AS350": {
        "vel_kt": 100, "valor_hora": 9788.57, "pax": "04 Pax",
        "tipo_sigla": "ESQUILO", "is_heli": True,
    },
}

# ---------------------------------------------------------------------------
# COORDENADAS DE EMERGÊNCIA (último recurso)
# ---------------------------------------------------------------------------
# A fonte primária é o arquivo local coordenadas_aerodromos.json, gerado pelo
# script gerar_coordenadas.py e versionado no repositório. Este dicionário só
# entra em ação se o arquivo não existir E a internet estiver indisponível.
# ---------------------------------------------------------------------------
COORDS_BACKUP = {
    "SNGQ": {"lat": -19.7411, "lon": -45.2447}, "SIWH": {"lat": -18.4752, "lon": -47.1916},
    "SDNA": {"lat": -19.7616, "lon": -49.0763}, "SNXV": {"lat": -18.7613, "lon": -44.8988},
    "SSVG": {"lat": -20.7672, "lon": -45.9186}, "SNSR": {"lat": -17.7802, "lon": -47.0988},
    "SSDK": {"lat": -19.9547, "lon": -44.6069}, "SNLY": {"lat": -20.0219, "lon": -45.5458},
    "SWWM": {"lat": -18.0647, "lon": -40.9788}, "SSYF": {"lat": -18.8711, "lon": -48.8805},
    "SNTD": {"lat": -16.4858, "lon": -46.5413}, "SSYD": {"lat": -19.1416, "lon": -47.6780},
    "SWZT": {"lat": -19.2736, "lon": -44.4041}, "SIEX": {"lat": -18.8419, "lon": -50.1219},
    "SNJV": {"lat": -15.9344, "lon": -44.0105}, "SNFI": {"lat": -18.5908, "lon": -48.7052},
    "SSAT": {"lat": -17.9869, "lon": -46.9058}, "SNJN": {"lat": -15.4677, "lon": -44.3644},
    "SNBG": {"lat": -19.4672, "lon": -41.0119}, "SNAR": {"lat": -16.1683, "lon": -40.6694},
    "SNKD": {"lat": -19.0436, "lon": -43.4350}, "SNJI": {"lat": -17.2288, "lon": -44.4372},
    "SICK": {"lat": -17.6694, "lon": -42.5488}, "SNLG": {"lat": -19.5161, "lon": -43.7436},
    "SNEW": {"lat": -19.6894, "lon": -50.6866}, "SNUN": {"lat": -16.3565, "lon": -46.9277},
    "SIRS": {"lat": -19.7891, "lon": -48.5719}, "SDJR": {"lat": -19.4447, "lon": -44.2741},
    "SBAR": {"lat": -10.9838, "lon": -37.0733}, "SBBE": {"lat": -1.3792, "lon": -48.4761},
    "SBBV": {"lat": 2.8461, "lon": -60.6922}, "SBBR": {"lat": -15.8697, "lon": -47.9172},
    "SBCG": {"lat": -20.4686, "lon": -54.6724}, "SBCY": {"lat": -15.6527, "lon": -56.1166},
    "SBCT": {"lat": -25.5316, "lon": -49.1761}, "SBFL": {"lat": -27.6702, "lon": -48.5525},
    "SBFZ": {"lat": -3.7762, "lon": -38.5325}, "SBGO": {"lat": -16.6322, "lon": -49.2208},
    "SBGR": {"lat": -23.4355, "lon": -46.4730}, "SBJP": {"lat": -7.1483, "lon": -34.9505},
    "SBMQ": {"lat": 0.0505, "lon": -51.0722}, "SBMO": {"lat": -9.5108, "lon": -35.7916},
    "SBEG": {"lat": -3.0386, "lon": -60.0497}, "SBSG": {"lat": -5.7688, "lon": -35.3663},
    "SBPJ": {"lat": -10.2900, "lon": -48.3577}, "SBPA": {"lat": -29.9938, "lon": -51.1711},
    "SBPV": {"lat": -8.7136, "lon": -63.9027}, "SBRF": {"lat": -8.1263, "lon": -34.9230},
    "SBRB": {"lat": -9.8683, "lon": -67.8980}, "SBRJ": {"lat": -22.9104, "lon": -43.1631},
    "SBGL": {"lat": -22.8099, "lon": -43.2505}, "SBSV": {"lat": -12.9086, "lon": -38.3224},
    "SBSL": {"lat": -2.5869, "lon": -44.2361}, "SBSP": {"lat": -23.6261, "lon": -46.6563},
    "SBTE": {"lat": -5.0594, "lon": -42.8244}, "SBVT": {"lat": -20.2580, "lon": -40.2863},
}
