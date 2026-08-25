# -*- coding: utf-8 -*-
"""
Regras de tempo específicas do COMAVE.

Puro Python, sem Streamlit — testável por pytest.
Não altera nenhuma regra da DTA.
"""

from regras import velocidade_efetiva

# --- Acréscimos de solo ----------------------------------------------------
# Uma única soma por perna (táxi e providências pré-decolagem). Não se soma
# origem com destino: a perna recebe 25 min se tocar capital em qualquer uma
# das pontas, 15 min caso contrário, e 5 min quando for asa rotativa.
MIN_SOLO_AVIAO = 15          # perna sem capital
MIN_SOLO_AVIAO_CAPITAL = 25  # perna com capital na origem ou no destino
MIN_SOLO_HELI = 5            # asa rotativa, tocando capital ou não

# Aeroportos de capital nacional.
# ATENÇÃO: SBBH (Pampulha) e SBCF (Confins) NÃO estão nesta lista — ver o
# comentário em TEMPO_FIXO_COMAVE_MIN e a pendência registrada no README.
CAPITAIS_ICAO = frozenset({
    "SBAR", "SBBE", "SBBV", "SBBR", "SBCG", "SBCY", "SBCT", "SBFL", "SBFZ",
    "SBGO", "SBGR", "SBJP", "SBMQ", "SBMO", "SBEG", "SBSG", "SBPJ", "SBPA",
    "SBPV", "SBRF", "SBRB", "SBRJ", "SBGL", "SBSV", "SBSL", "SBSP", "SBTE",
    "SBVT",
})

# --- Trechos de tempo fixo -------------------------------------------------
# Pernas em que o tempo total é tabelado, substituindo o cálculo por distância.
# Neste caso o tempo É faturado (decisão do cliente).
TEMPO_FIXO_COMAVE_MIN = {frozenset({"SBBH", "SBCF"}): 15}


def perna_toca_capital(origem, destino):
    """True se a perna sai de ou chega a um aeroporto de capital nacional."""
    return origem in CAPITAIS_ICAO or destino in CAPITAIS_ICAO


def minutos_solo_perna(origem, destino, is_heli):
    """
    Acréscimo de solo da perna, em minutos. Uma única soma por perna:

      helicóptero .......... 5 min, tocando capital ou não
      avião com capital .... 25 min (capital na origem OU no destino)
      demais aviões ........ 15 min
    """
    if is_heli:
        return MIN_SOLO_HELI
    return MIN_SOLO_AVIAO_CAPITAL if perna_toca_capital(origem, destino) else MIN_SOLO_AVIAO


def tempo_fixo_minutos(origem, destino, tabela=None):
    """Minutos tabelados para o par origem/destino, ou None se não houver."""
    tabela = TEMPO_FIXO_COMAVE_MIN if tabela is None else tabela
    return tabela.get(frozenset({origem, destino}))


def calcular_tempos_comave(origem, destino, dados_aero, dist_nm):
    """
    Devolve um dicionário com a decomposição do tempo da perna:

      tempo_voo_h      -> horas de voo puro (decolagem a pouso)
      minutos_solo     -> acréscimo de solo exibido, não faturado
      tempo_total_h    -> o que aparece na coluna TEMPO da tabela
      horas_faturadas  -> o que multiplica o valor da hora
      tempo_fixo       -> True se a perna usou tempo tabelado

    Regra do faturamento: o tempo de solo entra no tempo exibido e NÃO entra
    no custo. A exceção é a perna de tempo fixo, integralmente faturada.
    """
    minutos_fixos = tempo_fixo_minutos(origem, destino)
    if minutos_fixos is not None:
        horas = minutos_fixos / 60
        return {
            "tempo_voo_h": horas,
            "minutos_solo": 0,
            "tempo_total_h": horas,
            "horas_faturadas": horas,
            "tempo_fixo": True,
            "vel_kt": 0,
        }

    vel_kt = velocidade_efetiva(dados_aero, dist_nm)
    tempo_voo_h = dist_nm / vel_kt if vel_kt > 0 else 0.0

    minutos_solo = minutos_solo_perna(origem, destino, dados_aero.get("is_heli", False))

    return {
        "tempo_voo_h": tempo_voo_h,
        "minutos_solo": minutos_solo,
        "tempo_total_h": tempo_voo_h + minutos_solo / 60,
        "horas_faturadas": tempo_voo_h,
        "tempo_fixo": False,
        "vel_kt": vel_kt,
    }


def valor_hora(contrato, aeronave_nome):
    """Valor da hora de voo da aeronave no contrato, ou None se não coberta."""
    return contrato["precos"].get(aeronave_nome)


def aeronaves_do_contrato(contrato, frota):
    """Aeronaves da frota cobertas pelo contrato, na ordem da frota."""
    return [nome for nome in frota if nome in contrato["precos"]]
