# -*- coding: utf-8 -*-
"""
Regra de tempo de solo — compartilhada pelas abas DTA e COMAVE.

Vive em módulo próprio de propósito: a regra de quanto tempo se soma é a
mesma nos dois clientes, mas o que cada um FAZ com esse tempo é diferente
(o COMAVE fatura, a DTA só exibe). Manter a regra aqui evita que a aba DTA
precise importar qualquer coisa do módulo do COMAVE.

Uma única soma por perna: não se acumula origem com destino.
    helicóptero .......... 5 min, tocando capital ou não
    avião com capital .... 25 min (capital na origem OU no destino)
    demais aviões ........ 15 min
"""

MIN_SOLO_AVIAO = 15          # perna sem capital
MIN_SOLO_AVIAO_CAPITAL = 25  # perna com capital na origem ou no destino
MIN_SOLO_HELI = 5            # asa rotativa, tocando capital ou não

# Aeroportos de capital nacional.
# ATENÇÃO: SBBH (Pampulha) e SBCF (Confins) NÃO estão nesta lista — decisão
# pendente de confirmação, registrada no README.
CAPITAIS_ICAO = frozenset({
    "SBAR", "SBBE", "SBBV", "SBBR", "SBCG", "SBCY", "SBCT", "SBFL", "SBFZ",
    "SBGO", "SBGR", "SBJP", "SBMQ", "SBMO", "SBEG", "SBSG", "SBPJ", "SBPA",
    "SBPV", "SBRF", "SBRB", "SBRJ", "SBGL", "SBSV", "SBSL", "SBSP", "SBTE",
    "SBVT",
})

# Texto exibido ao pé da tabela sempre que o acréscimo estiver aplicado.
MSG_ACRESCIMO_SOLO = (
    "Tempo exibido inclui o acréscimo de solo (15 min por aeroporto, "
    "25 min se capital, 5 min por perna de helicóptero)."
)


def perna_toca_capital(origem, destino):
    """True se a perna sai de ou chega a um aeroporto de capital nacional."""
    return origem in CAPITAIS_ICAO or destino in CAPITAIS_ICAO


def minutos_solo_perna(origem, destino, is_heli):
    """Acréscimo de solo da perna, em minutos. Uma única soma por perna."""
    if is_heli:
        return MIN_SOLO_HELI
    return MIN_SOLO_AVIAO_CAPITAL if perna_toca_capital(origem, destino) else MIN_SOLO_AVIAO
