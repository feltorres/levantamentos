# -*- coding: utf-8 -*-
"""
Regras de negócio e motor de cálculo do Planejador de Missões Aéreas - DTA.

Nenhuma função aqui importa Streamlit ou toca em interface. É de propósito:
tudo neste arquivo é testável por pytest sem subir a aplicação web.
"""

import math
import re

RAIO_TERRA_NM = 3440.065  # raio médio da Terra em milhas náuticas (NM)

# Termos que, se aparecerem no campo "pista", indicam restrição regulatória
TERMOS_RESTRICAO_ANAC = ("FECHADO PELA ANAC", "NÃO HOMOLOGADO", "NÃO OPERACIONAL")

# Tipos de bloqueio devolvidos por verifica_restricao_pista
BLOQUEIO_PISTA = "PISTA"
BLOQUEIO_ANAC = "ANAC"


def calcular_distancia_nm(lat1, lon1, lat2, lon2):
    """Distância ortodrômica (círculo máximo) em milhas náuticas, 1 casa decimal."""
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    )
    # clamp: erro de ponto flutuante pode empurrar 'a' um fio acima de 1.0
    # e math.asin(sqrt(a)) estouraria com ValueError em antípodas
    a = min(1.0, max(0.0, a))
    return round(RAIO_TERRA_NM * (2 * math.asin(math.sqrt(a))), 1)


def comprimento_pista(pista_str):
    """
    Extrai o comprimento em metros do texto da pista.
    "1200 x 30" -> 1200 | "NÃO HOMOLOGADO" -> None | "" -> None
    """
    match = re.match(r"\s*(\d+)", str(pista_str))
    return int(match.group(1)) if match else None


def velocidade_efetiva(dados_aero, dist_nm):
    """
    Velocidade a aplicar na perna, em nós (KT).

    Regra de tabela dupla (King Air B200, por definição da chefia): se o tempo
    calculado na velocidade base atingir 1 hora, a perna INTEIRA passa a ser
    calculada na velocidade da 2ª tabela.

    ATENÇÃO — comportamento conhecido e mantido intencionalmente: a regra é
    descontínua. Em 199 NM o voo custa mais caro que em 200 NM. Não é bug de
    código, é a tabela vigente do operador. Se a chefia revisar, mexer só aqui.
    """
    vel_base = dados_aero.get("vel_kt", 0)
    if not dados_aero.get("regra_tabela_dupla") or vel_base <= 0:
        return vel_base

    tempo_base = dist_nm / vel_base
    if tempo_base >= 1.0:
        return dados_aero.get("vel_kt_t2", vel_base)
    return vel_base


def decimal_para_hhmmss(tempo_decimal):
    """0.5 -> '00:30:00'. Trata o carry de 59,7 s -> 60 s."""
    if tempo_decimal is None or tempo_decimal < 0:
        return "00:00:00"

    horas = int(tempo_decimal)
    minutos_dec = (tempo_decimal - horas) * 60
    minutos = int(minutos_dec)
    segundos = round((minutos_dec - minutos) * 60)

    if segundos == 60:
        segundos = 0
        minutos += 1
    if minutos == 60:
        minutos = 0
        horas += 1

    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


def verifica_restricao_pista(local_id, aeronave_nome, dados_aero, dados_local):
    """
    Avalia se a aeronave pode operar na localidade.

    Retorna (bloqueado: bool, mensagem: str, tipo: str)
      tipo == BLOQUEIO_PISTA -> erro duro, aborta o cálculo da missão
      tipo == BLOQUEIO_ANAC  -> erro brando, a linha aparece na tabela sem custo
    """
    if dados_local is None:
        return True, f"LOCALIDADE NÃO ENCONTRADA NA BASE ({local_id})", BLOQUEIO_PISTA

    is_heli = dados_aero.get("is_heli", False)

    # 1) Área livre (cidade sem aeródromo): só asa rotativa
    if dados_local.get("is_extra"):
        if not is_heli:
            return (
                True,
                f"AERONAVE DE ASA FIXA ({aeronave_nome}) NÃO PODE OPERAR EM ÁREA LIVRE "
                f"({dados_local.get('cidade', local_id)})",
                BLOQUEIO_PISTA,
            )
        return False, "", ""

    pista_str = str(dados_local.get("pista", "")).upper()

    # 2) Restrição regulatória (ANAC - Agência Nacional de Aviação Civil)
    restrito_por_texto = any(termo in pista_str for termo in TERMOS_RESTRICAO_ANAC)
    if (dados_local.get("restricao_anac") or restrito_por_texto) and not is_heli:
        return True, f"AEROPORTO INOPERANTE/NÃO HOMOLOGADO ({local_id})", BLOQUEIO_ANAC

    # 3) Comprimento mínimo de pista
    if dados_aero.get("requer_pista_1200") and not is_heli:
        comprimento = comprimento_pista(pista_str)
        if comprimento is None:
            return (
                True,
                f"AERONAVE ({aeronave_nome}) NÃO PODE OPERAR NESTA PISTA "
                f"({local_id} - dimensão não informada)",
                BLOQUEIO_PISTA,
            )
        if comprimento < 1200:
            return (
                True,
                f"AERONAVE ({aeronave_nome}) NÃO PODE OPERAR NESTA PISTA "
                f"({local_id} - {comprimento}m)",
                BLOQUEIO_PISTA,
            )

    return False, "", ""


def aeronaves_aptas(local_id, dados_local, frota):
    """Lista os nomes das aeronaves da frota que podem operar na localidade."""
    aptas = []
    for nome, dados_aero in frota.items():
        bloqueado, _, _ = verifica_restricao_pista(local_id, nome, dados_aero, dados_local)
        if not bloqueado:
            aptas.append(nome)
    return aptas


def formatar_brl(valor):
    """1234.5 -> 'R$ 1.234,50'"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
