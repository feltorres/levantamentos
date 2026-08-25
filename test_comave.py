# -*- coding: utf-8 -*-
"""
Testes das tabelas de custo e regras de tempo do COMAVE.

Sete tabelas de preço são sete oportunidades de digitar um número errado.
Cada valor da Nota Técnica nº 21 está conferido abaixo, um a um.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest  # noqa: E402

from dados import FROTA  # noqa: E402
from dados_comave import CONTRATOS, FROTA_COMAVE  # noqa: E402
from regras_comave import (  # noqa: E402
    MIN_SOLO_AVIAO,
    MIN_SOLO_AVIAO_CAPITAL,
    MIN_SOLO_HELI,
    aeronaves_do_contrato,
    calcular_tempos_comave,
    minutos_solo_perna,
    perna_toca_capital,
    tempo_fixo_minutos,
    valor_hora,
)

ESQUILO = FROTA_COMAVE["Esquilo AS350"]
C90 = FROTA_COMAVE["King Air C90 (PR/PT-OSO)"]
B200 = FROTA_COMAVE["King Air B200 (PTWGS)"]


# --- Tempo de solo ---------------------------------------------------------
def test_perna_sem_capital_recebe_15_minutos():
    t = calcular_tempos_comave("SNDV", "SNPD", C90, 200)
    assert t["minutos_solo"] == MIN_SOLO_AVIAO == 15


def test_capital_na_origem_gera_25_minutos():
    t = calcular_tempos_comave("SBBR", "SNPD", C90, 200)
    assert t["minutos_solo"] == MIN_SOLO_AVIAO_CAPITAL == 25


def test_capital_no_destino_tambem_gera_25_minutos():
    t = calcular_tempos_comave("SNDV", "SBBR", C90, 200)
    assert t["minutos_solo"] == 25


def test_perna_entre_capitais_nao_soma_duas_vezes():
    """25 min é o teto da perna: origem e destino não se acumulam."""
    t = calcular_tempos_comave("SBBR", "SBSP", C90, 400)
    assert t["minutos_solo"] == 25


def test_pampulha_e_confins_nao_contam_como_capital():
    # PENDENTE DE CONFIRMAÇÃO: ver o README. Se a decisão mudar, basta
    # incluir SBBH e SBCF em CAPITAIS_ICAO — este teste denuncia a mudança.
    assert perna_toca_capital("SBBH", "SNPD") is False
    assert perna_toca_capital("SBCF", "SNPD") is False
    assert calcular_tempos_comave("SBBH", "SNPD", C90, 200)["minutos_solo"] == 15


def test_helicoptero_recebe_5_minutos_em_qualquer_perna():
    sem_capital = calcular_tempos_comave("SNDV", "SNPD", ESQUILO, 200)
    com_capital = calcular_tempos_comave("SBBR", "SBSP", ESQUILO, 400)
    assert sem_capital["minutos_solo"] == com_capital["minutos_solo"] == MIN_SOLO_HELI == 5


def test_minutos_solo_perna_direto():
    assert minutos_solo_perna("SNDV", "SNPD", False) == 15
    assert minutos_solo_perna("SNDV", "SBGL", False) == 25
    assert minutos_solo_perna("SBGL", "SBSP", True) == 5


def test_tempo_de_solo_entra_no_total_exibido():
    t = calcular_tempos_comave("SNDV", "SNPD", C90, 200)
    assert t["tempo_total_h"] == pytest.approx(t["tempo_voo_h"] + 15 / 60)


def test_tempo_de_solo_e_faturado_no_comave():
    """No COMAVE o solo entra no custo: tempo exibido e faturado são o mesmo."""
    t = calcular_tempos_comave("SNDV", "SNPD", C90, 200)
    assert t["horas_faturadas"] == pytest.approx(t["tempo_total_h"])
    assert t["horas_faturadas"] > t["tempo_voo_h"]


def test_custo_comave_reflete_o_tempo_exibido():
    preco = 12000.0
    t = calcular_tempos_comave("SNDV", "SBBR", C90, 200)  # 25 min de solo
    assert t["horas_faturadas"] * preco == pytest.approx((t["tempo_voo_h"] + 25 / 60) * preco)


# --- Trecho de tempo fixo --------------------------------------------------
def test_bh_confins_tem_15_minutos_no_comave():
    assert tempo_fixo_minutos("SBBH", "SBCF") == 15


def test_bh_confins_vale_nos_dois_sentidos():
    assert tempo_fixo_minutos("SBCF", "SBBH") == 15


def test_outros_pares_nao_tem_tempo_fixo():
    assert tempo_fixo_minutos("SBBH", "SBBR") is None


def test_trecho_fixo_e_integralmente_faturado():
    t = calcular_tempos_comave("SBBH", "SBCF", C90, 13.1)
    assert t["tempo_fixo"] is True
    assert t["tempo_total_h"] == pytest.approx(15 / 60)
    assert t["horas_faturadas"] == pytest.approx(15 / 60)
    assert t["minutos_solo"] == 0


def test_trecho_fixo_ignora_distancia_e_aeronave():
    lento = calcular_tempos_comave("SBBH", "SBCF", ESQUILO, 13.1)
    rapido = calcular_tempos_comave("SBBH", "SBCF", B200, 13.1)
    assert lento["tempo_total_h"] == rapido["tempo_total_h"] == pytest.approx(15 / 60)


# --- Regra do B200 na aba COMAVE -------------------------------------------
def test_b200_mantem_a_tabela_dupla_no_comave():
    curto = calcular_tempos_comave("SNDV", "SNPD", B200, 199)
    longo = calcular_tempos_comave("SNDV", "SNPD", B200, 200)
    assert curto["vel_kt"] == 200
    assert longo["vel_kt"] == 225


def test_gatilho_do_b200_usa_tempo_de_voo_e_nao_o_solo():
    # 190 NM a 200 KT = 0,95 h de voo; com 15 min de solo passaria de 1 h,
    # mas o gatilho olha só o voo, então continua na primeira tabela.
    t = calcular_tempos_comave("SNDV", "SNPD", B200, 190)
    assert t["vel_kt"] == 200
    assert t["tempo_total_h"] > 1.0


# --- Tabelas de preço: conferência valor a valor ---------------------------
PADRAO = "TJM MG — Tribunal de Justiça Militar (TDCO)"


@pytest.mark.parametrize("aeronave,esperado", [
    ("Esquilo AS350", 9900.00),
    ("Dauphin N2 (PP-EPO)", 16500.00),
    ("Dauphin N3 (PR-DTG)", 16500.00),
    ("King Air C90 (PR/PT-OSO)", 13750.00),
    ("King Air B200 (PTWGS)", 13750.00),
    ("King Air B300 (PP-EJO)", 13750.00),
    ("King Air B350 (PR-XAA)", 13750.00),
    ("Citation Bravo", 31900.00),
])
def test_tabela_padrao(aeronave, esperado):
    assert valor_hora(CONTRATOS[PADRAO], aeronave) == esperado


def test_seis_orgaos_compartilham_a_tabela_padrao():
    iguais = [
        "TJM MG — Tribunal de Justiça Militar (TDCO)",
        "TJMG — Tribunal de Justiça de MG (Convênio)",
        "SES — Saúde em geral (TDCO SES 1)",
        "CEMIG (Convênio)",
        "COPASA (Convênio)",
    ]
    referencia = CONTRATOS[iguais[0]]["precos"]
    for nome in iguais[1:]:
        assert CONTRATOS[nome]["precos"] == referencia
    # Uberlândia usa o mesmo valor de Esquilo, mas só cobre essa aeronave
    uber = CONTRATOS["Uberlândia — Sec. Municipal de Saúde"]
    assert uber["precos"]["Esquilo AS350"] == referencia["Esquilo AS350"]
    assert list(uber["precos"]) == ["Esquilo AS350"]


@pytest.mark.parametrize("aeronave,esperado", [
    ("Esquilo AS350", 8750.00),
    ("Dauphin N2 (PP-EPO)", 10000.00),
    ("King Air C90 (PR/PT-OSO)", 8750.00),
    ("King Air B200 (PTWGS)", 9000.00),
    ("King Air B300 (PP-EJO)", 12000.00),
    ("Citation Bravo", 12000.00),
])
def test_tabela_fhemig(aeronave, esperado):
    assert valor_hora(CONTRATOS["FHEMIG — MG Transplantes (TDCO)"], aeronave) == esperado


@pytest.mark.parametrize("aeronave,esperado", [
    ("Esquilo AS350", 11307.82),
    ("Dauphin N3 (PR-DTG)", 29440.91),
    ("King Air C90 (PR/PT-OSO)", 9055.37),
    ("King Air B200 (PTWGS)", 12563.06),
    ("King Air B300 (PP-EJO)", 15729.80),
    ("Citation Bravo", 21276.38),
])
def test_tabela_seapa(aeronave, esperado):
    assert valor_hora(CONTRATOS["SEAPA — Secretaria de Agricultura"], aeronave) == esperado


@pytest.mark.parametrize("aeronave,esperado", [
    ("Esquilo AS350", 11044.86),
    ("Dauphin N3 (PR-DTG)", 27788.01),
    ("King Air C90 (PR/PT-OSO)", 7859.79),
    ("King Air B200 (PTWGS)", 11621.02),
    ("King Air B300 (PP-EJO)", 14135.34),
    ("Citation Bravo", 20644.58),
])
def test_tabela_ses2(aeronave, esperado):
    assert valor_hora(CONTRATOS["SES 2 — MG Transplantes (TDCO)"], aeronave) == esperado


@pytest.mark.parametrize("aeronave,esperado", [
    ("Esquilo AS350", 10216.36),
    ("Dauphin N3 (PR-DTG)", 27090.64),
    ("King Air C90 (PR/PT-OSO)", 7162.42),
    ("King Air B200 (PTWGS)", 10923.65),
    ("King Air B300 (PP-EJO)", 13437.97),
    ("Citation Bravo", 19947.21),
])
def test_tabela_gmg_13a(aeronave, esperado):
    assert valor_hora(CONTRATOS["GMG/PMMG — Gestão da frota (Tabela 13A)"], aeronave) == esperado


@pytest.mark.parametrize("aeronave,esperado", [
    ("King Air C90 (PR/PT-OSO)", 9055.37),
    ("King Air B200 (PTWGS)", 12563.06),
    ("King Air B300 (PP-EJO)", 15729.80),
])
def test_tabela_pbh(aeronave, esperado):
    assert valor_hora(CONTRATOS["PBH — Prefeitura de Belo Horizonte"], aeronave) == esperado


@pytest.mark.parametrize("aeronave,esperado", [
    ("Esquilo AS350", 8000.00),
    ("King Air C90 (PR/PT-OSO)", 8000.00),
    ("King Air B200 (PTWGS)", 9000.00),
    ("King Air B300 (PP-EJO)", 12000.00),
    ("Dauphin N2 (PP-EPO)", 14000.00),
])
def test_tabela_cbm_ipsm(aeronave, esperado):
    assert valor_hora(CONTRATOS["CBM/PMMG/IPSM (Convênio)"], aeronave) == esperado


# --- Cobertura contratual --------------------------------------------------
def test_pbh_cobre_apenas_king_air():
    aptas = aeronaves_do_contrato(CONTRATOS["PBH — Prefeitura de Belo Horizonte"], FROTA_COMAVE)
    assert all("King Air" in nome for nome in aptas)
    assert len(aptas) == 4


def test_uberlandia_cobre_apenas_esquilo():
    aptas = aeronaves_do_contrato(
        CONTRATOS["Uberlândia — Sec. Municipal de Saúde"], FROTA_COMAVE
    )
    assert aptas == ["Esquilo AS350"]


def test_cbm_nao_tem_jato():
    aptas = aeronaves_do_contrato(CONTRATOS["CBM/PMMG/IPSM (Convênio)"], FROTA_COMAVE)
    assert "Citation Bravo" not in aptas


def test_aeronave_fora_do_contrato_devolve_none():
    assert valor_hora(CONTRATOS["PBH — Prefeitura de Belo Horizonte"], "Esquilo AS350") is None


def test_citation_vii_nao_existe_em_lugar_nenhum():
    for contrato in CONTRATOS.values():
        for aeronave in contrato["precos"]:
            assert "VII" not in aeronave and "C650" not in aeronave


def test_dauphin_fhemig_e_muito_mais_barato_que_ses2():
    """
    Armadilha real: FHEMIG e SES 2 atendem o MG Transplantes com tabelas
    diferentes. Clicar no contrato errado quase triplica o valor do Dauphin.
    """
    fhemig = valor_hora(CONTRATOS["FHEMIG — MG Transplantes (TDCO)"], "Dauphin N3 (PR-DTG)")
    ses2 = valor_hora(CONTRATOS["SES 2 — MG Transplantes (TDCO)"], "Dauphin N3 (PR-DTG)")
    assert ses2 > fhemig * 2.5


# --- Integridade -----------------------------------------------------------
def test_todo_contrato_tem_metadados():
    for nome, contrato in CONTRATOS.items():
        for campo in ("sei", "vigencia", "item_nt", "precos"):
            assert campo in contrato, f"{nome} sem o campo '{campo}'"
        assert contrato["precos"], f"{nome} sem nenhum preço"


def test_todo_preco_referencia_aeronave_existente():
    for nome, contrato in CONTRATOS.items():
        for aeronave in contrato["precos"]:
            assert aeronave in FROTA_COMAVE, f"{nome}: aeronave desconhecida '{aeronave}'"


def test_todo_preco_e_positivo():
    for nome, contrato in CONTRATOS.items():
        for aeronave, preco in contrato["precos"].items():
            assert preco > 0, f"{nome}/{aeronave} com valor inválido"


def test_velocidades_batem_com_a_frota_da_dta():
    """Canário: mesma aeronave física, mesma velocidade nos dois módulos."""
    for nome, dados in FROTA_COMAVE.items():
        assert nome in FROTA, f"{nome} não existe na frota DTA"
        assert dados["vel_kt"] == FROTA[nome]["vel_kt"], f"velocidade divergente em {nome}"
        assert dados["is_heli"] == FROTA[nome]["is_heli"], f"tipo divergente em {nome}"


def test_tabelas_comave_nao_contaminam_a_frota_dta():
    """A frota DTA mantém seus próprios valores/hora, isolados do COMAVE."""
    assert FROTA["Esquilo AS350"]["valor_hora"] == 9788.57
    assert FROTA["King Air B300 (PP-EJO)"]["valor_hora"] == 9705.13
    assert all("valor_hora" not in dados for dados in FROTA_COMAVE.values())
