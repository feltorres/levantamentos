# -*- coding: utf-8 -*-
"""
Regras de tempo específicas do COMAVE.

Puro Python, sem Streamlit — testável por pytest.
Não altera nenhuma regra da DTA.
"""

from regras import velocidade_efetiva

# --- Acréscimos de solo ----------------------------------------------------
# A regra vive em regras_solo.py, compartilhada com a aba DTA. Aqui só se
# define o que o COMAVE faz com ela: o tempo de solo É FATURADO.
from regras_solo import (  # noqa: E402  (reexportado por conveniência)
    CAPITAIS_ICAO,
    MIN_SOLO_AVIAO,
    MIN_SOLO_AVIAO_CAPITAL,
    MIN_SOLO_HELI,
    MSG_ACRESCIMO_SOLO,
    minutos_solo_perna,
    perna_toca_capital,
)

# --- Trechos de tempo fixo -------------------------------------------------
# Pernas em que o tempo total é tabelado, substituindo o cálculo por distância.
# Neste caso o tempo É faturado (decisão do cliente).
TEMPO_FIXO_COMAVE_MIN = {frozenset({"SBBH", "SBCF"}): 15}


def tempo_fixo_minutos(origem, destino, tabela=None):
    """Minutos tabelados para o par origem/destino, ou None se não houver."""
    tabela = TEMPO_FIXO_COMAVE_MIN if tabela is None else tabela
    return tabela.get(frozenset({origem, destino}))


def calcular_tempos_comave(origem, destino, dados_aero, dist_nm):
    """
    Devolve um dicionário com a decomposição do tempo da perna:

      tempo_voo_h      -> horas de voo puro (decolagem a pouso)
      minutos_solo     -> acréscimo de solo da perna
      tempo_total_h    -> o que aparece na coluna TEMPO da tabela
      horas_faturadas  -> o que multiplica o valor da hora
      tempo_fixo       -> True se a perna usou tempo tabelado

    Regra do faturamento no COMAVE: o tempo de solo É FATURADO — custo e
    tempo exibido saem do mesmo número. Difere da aba DTA, onde o acréscimo
    é opcional e nunca entra no custo.
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

    tempo_total_h = tempo_voo_h + minutos_solo / 60
    return {
        "tempo_voo_h": tempo_voo_h,
        "minutos_solo": minutos_solo,
        "tempo_total_h": tempo_total_h,
        "horas_faturadas": tempo_total_h,
        "tempo_fixo": False,
        "vel_kt": vel_kt,
    }


def valor_hora(contrato, aeronave_nome):
    """Valor da hora de voo da aeronave no contrato, ou None se não coberta."""
    return contrato["precos"].get(aeronave_nome)


def aeronaves_do_contrato(contrato, frota):
    """Aeronaves da frota cobertas pelo contrato, na ordem da frota."""
    return [nome for nome in frota if nome in contrato["precos"]]
