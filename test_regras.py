# -*- coding: utf-8 -*-
"""
Suíte de regressão das regras de negócio.

Rodar na raiz do projeto:
    pip install pytest
    pytest -v
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest  # noqa: E402

from dados import AEROPORTOS, FROTA  # noqa: E402
from regras import (  # noqa: E402
    BLOQUEIO_ANAC,
    BLOQUEIO_PISTA,
    calcular_distancia_nm,
    comprimento_pista,
    decimal_para_hhmmss,
    formatar_brl,
    velocidade_efetiva,
    verifica_restricao_pista,
)

CITATION = FROTA["Citation Bravo"]
B200 = FROTA["King Air B200 (PTWGS)"]
ESQUILO = FROTA["Esquilo AS350"]
C90 = FROTA["King Air C90 (PR/PT-OSO)"]

AREA_LIVRE = {"cidade": "Cidade Sem Pista", "uf": "MG", "pista": "Área Livre/Campo",
              "op_noturna": "Não", "lat": -19.0, "lon": -44.0, "is_extra": True}


# --- Distância -------------------------------------------------------------
def test_distancia_mesmo_ponto_eh_zero():
    assert calcular_distancia_nm(-19.85, -43.95, -19.85, -43.95) == 0.0


def test_distancia_bh_confins_plausivel():
    # SBBH -> SBCF: cerca de 20 NM
    d = calcular_distancia_nm(-19.8512, -43.9506, -19.6244, -43.9719)
    assert 10 < d < 30


def test_distancia_antipodas_nao_estoura():
    # sem o clamp em asin(sqrt(a)), este caso levantava ValueError
    assert calcular_distancia_nm(0.0, 0.0, 0.0, 180.0) > 10000


def test_distancia_eh_simetrica():
    ida = calcular_distancia_nm(-19.85, -43.95, -15.87, -47.92)
    volta = calcular_distancia_nm(-15.87, -47.92, -19.85, -43.95)
    assert ida == volta


# --- Comprimento de pista --------------------------------------------------
@pytest.mark.parametrize(
    "texto,esperado",
    [
        ("1200 x 30", 1200),
        ("902 x 24", 902),
        ("NÃO HOMOLOGADO", None),
        ("", None),
        ("Área Livre/Campo", None),
    ],
)
def test_comprimento_pista(texto, esperado):
    assert comprimento_pista(texto) == esperado


# --- Velocidade / tabela dupla do B200 -------------------------------------
def test_b200_abaixo_de_uma_hora_usa_tabela_1():
    assert velocidade_efetiva(B200, 199) == 200


def test_b200_em_uma_hora_exata_usa_tabela_2():
    assert velocidade_efetiva(B200, 200) == 225


def test_b200_acima_de_uma_hora_usa_tabela_2():
    assert velocidade_efetiva(B200, 400) == 225


def test_aeronave_sem_tabela_dupla_ignora_a_regra():
    assert velocidade_efetiva(C90, 1000) == 200


def test_b200_descontinuidade_documentada():
    """
    Comportamento intencional (definição da chefia): 200 NM sai mais barato que
    199 NM. Se este teste falhar, alguém mexeu na regra — confirmar com a
    chefia antes de aceitar a mudança.
    """
    custo_199 = (199 / velocidade_efetiva(B200, 199)) * B200["valor_hora"]
    custo_200 = (200 / velocidade_efetiva(B200, 200)) * B200["valor_hora"]
    assert custo_200 < custo_199


# --- Conversão de tempo ----------------------------------------------------
@pytest.mark.parametrize(
    "decimal,esperado",
    [
        (0.0, "00:00:00"),
        (0.5, "00:30:00"),
        (1.0, "01:00:00"),
        (2.25, "02:15:00"),
        (0.9999999, "01:00:00"),  # carry de 59,99 s
    ],
)
def test_decimal_para_hhmmss(decimal, esperado):
    assert decimal_para_hhmmss(decimal) == esperado


# --- Restrições ------------------------------------------------------------
def test_citation_bloqueado_em_pista_curta():
    bloqueado, _, tipo = verifica_restricao_pista(
        "SNKF", "Citation Bravo", CITATION, AEROPORTOS["SNKF"]
    )
    assert bloqueado and tipo in (BLOQUEIO_PISTA, BLOQUEIO_ANAC)


def test_citation_liberado_em_pista_longa():
    bloqueado, _, _ = verifica_restricao_pista(
        "SBCF", "Citation Bravo", CITATION, AEROPORTOS["SBCF"]
    )
    assert not bloqueado


def test_c90_nao_tem_exigencia_de_pista_minima():
    bloqueado, _, _ = verifica_restricao_pista(
        "SNKD", "King Air C90 (PR/PT-OSO)", C90, AEROPORTOS["SNKD"]
    )  # SNKD tem 960 m
    assert not bloqueado


def test_aviao_em_aeroporto_com_restricao_anac_gera_bloqueio_brando():
    bloqueado, _, tipo = verifica_restricao_pista(
        "SNJN", "King Air C90 (PR/PT-OSO)", C90, AEROPORTOS["SNJN"]
    )
    assert bloqueado and tipo == BLOQUEIO_ANAC


def test_helicoptero_ignora_restricao_anac():
    bloqueado, _, _ = verifica_restricao_pista(
        "SNJN", "Esquilo AS350", ESQUILO, AEROPORTOS["SNJN"]
    )
    assert not bloqueado


def test_helicoptero_ignora_pista_minima():
    bloqueado, _, _ = verifica_restricao_pista(
        "SNKF", "Esquilo AS350", ESQUILO, AEROPORTOS["SNKF"]
    )
    assert not bloqueado


def test_asa_fixa_nao_opera_em_area_livre():
    bloqueado, _, tipo = verifica_restricao_pista(
        "Cidade Sem Pista", "Citation Bravo", CITATION, AREA_LIVRE
    )
    assert bloqueado and tipo == BLOQUEIO_PISTA


def test_helicoptero_opera_em_area_livre():
    bloqueado, _, _ = verifica_restricao_pista(
        "Cidade Sem Pista", "Esquilo AS350", ESQUILO, AREA_LIVRE
    )
    assert not bloqueado


def test_localidade_inexistente_bloqueia_sem_estourar():
    bloqueado, msg, tipo = verifica_restricao_pista("XXXX", "Esquilo AS350", ESQUILO, None)
    assert bloqueado and tipo == BLOQUEIO_PISTA and "XXXX" in msg


# --- Integridade da base ---------------------------------------------------
def test_todo_aerodromo_tem_campos_obrigatorios():
    for icao, dados in AEROPORTOS.items():
        for campo in ("cidade", "uf", "pista", "op_noturna"):
            assert campo in dados, f"{icao} sem o campo '{campo}'"


def test_toda_aeronave_tem_campos_obrigatorios():
    for nome, dados in FROTA.items():
        for campo in ("vel_kt", "valor_hora", "pax", "tipo_sigla", "is_heli"):
            assert campo in dados, f"{nome} sem o campo '{campo}'"
        assert dados["vel_kt"] > 0
        assert dados["valor_hora"] > 0
        if dados.get("regra_tabela_dupla"):
            assert "vel_kt_t2" in dados, f"{nome} usa tabela dupla sem vel_kt_t2"


def test_siglas_de_aeronave_sao_unicas():
    siglas = [d["tipo_sigla"] for d in FROTA.values()]
    assert len(siglas) == len(set(siglas)), "duas aeronaves compartilham a mesma sigla"


def test_codigos_icao_tem_quatro_letras():
    for icao in AEROPORTOS:
        assert len(icao) == 4 and icao.isalnum(), f"código ICAO suspeito: {icao}"


# --- Formatação ------------------------------------------------------------
def test_formatar_brl():
    assert formatar_brl(1234.5) == "R$ 1.234,50"
    assert formatar_brl(0) == "R$ 0,00"
    assert formatar_brl(1000000) == "R$ 1.000.000,00"


# --- Trecho de tempo fixo na DTA (BH x Confins) ----------------------------
def test_bh_confins_tem_10_minutos_na_dta():
    from regras import tempo_fixo_dta_minutos
    assert tempo_fixo_dta_minutos("SBBH", "SBCF") == 10


def test_bh_confins_dta_vale_nos_dois_sentidos():
    from regras import tempo_fixo_dta_minutos
    assert tempo_fixo_dta_minutos("SBCF", "SBBH") == 10


def test_outros_pares_nao_tem_tempo_fixo_na_dta():
    from regras import tempo_fixo_dta_minutos
    assert tempo_fixo_dta_minutos("SBBH", "SBBR") is None
    assert tempo_fixo_dta_minutos("SBCF", "SBUL") is None


def test_tempo_fixo_dta_difere_do_comave():
    """DTA usa 10 min no par BH x Confins; COMAVE usa 15. Não podem convergir."""
    from regras import tempo_fixo_dta_minutos
    from regras_comave import tempo_fixo_minutos
    assert tempo_fixo_dta_minutos("SBBH", "SBCF") == 10
    assert tempo_fixo_minutos("SBBH", "SBCF") == 15
