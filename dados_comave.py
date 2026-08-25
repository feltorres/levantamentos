# -*- coding: utf-8 -*-
"""
Tabelas de custo do COMAVE — Comando de Aviação do Estado (PMMG).

FONTE: Nota Técnica nº 21/PMMG/COMAVE 4 - TDCO/CONV./2026
       Processo SEI nº 1250.01.0003379/2025-76 (doc. SEI nº 144797834)
       Atualizada em 17/07/2026, assinada por Fábio Simão Teixeira, 1º TEN PM.

ISOLAMENTO: este módulo NÃO tem relação com dados.py. Os valores da DTA e os
valores do COMAVE são de clientes diferentes e coincidências numéricas entre
eles são coincidências — nunca motivo para unificar. Mexer aqui não pode
alterar a aba DTA, e vice-versa.

O Citation VII (C650, PTMGS) foi vendido e por isso não consta de nenhuma
tabela, ainda que a Nota Técnica o mencione.

A tabela da FHEMIG (item "b" da Nota Técnica) foi removida a pedido do cliente
por não ser mais necessária. O contrato segue existindo no documento de origem;
se voltar a ser preciso, recuperar do histórico do Git.
"""

# ---------------------------------------------------------------------------
# FROTA COMAVE
# ---------------------------------------------------------------------------
# Velocidades e características replicadas da frota DTA — é a mesma aeronave
# física. A duplicação é proposital (isolamento entre os dois clientes); há um
# teste que denuncia qualquer divergência futura entre as duas listas.
# O valor da hora NÃO vive aqui: ele depende do órgão/contrato selecionado.
# ---------------------------------------------------------------------------
FROTA_COMAVE = {
    "Citation Bravo": {
        "vel_kt": 290, "pax": "07 Pax", "requer_pista_1200": True,
        "tipo_sigla": "JATO", "is_heli": False,
    },
    "King Air B350 (PR-XAA)": {
        "vel_kt": 220, "pax": "09 Pax", "tipo_sigla": "B350", "is_heli": False,
    },
    "King Air B300 (PP-EJO)": {
        "vel_kt": 220, "pax": "09 Pax", "tipo_sigla": "B300", "is_heli": False,
    },
    "King Air B200 (PTWGS)": {
        "vel_kt": 200, "vel_kt_t2": 225, "regra_tabela_dupla": True,
        "pax": "07 Pax", "tipo_sigla": "B200", "is_heli": False,
    },
    "King Air C90 (PR/PT-OSO)": {
        "vel_kt": 200, "pax": "06 Pax", "tipo_sigla": "C90", "is_heli": False,
    },
    "Dauphin N3 (PR-DTG)": {
        "vel_kt": 110, "pax": "05 Pax", "tipo_sigla": "DAUPHIN N3", "is_heli": True,
    },
    "Dauphin N2 (PP-EPO)": {
        "vel_kt": 110, "pax": "05 Pax", "tipo_sigla": "DAUPHIN N2", "is_heli": True,
    },
    "Esquilo AS350": {
        "vel_kt": 100, "pax": "04 Pax", "tipo_sigla": "ESQUILO", "is_heli": True,
    },
}

# ---------------------------------------------------------------------------
# TABELAS DE PREÇO (valor da hora de voo, em reais)
# ---------------------------------------------------------------------------
# Aeronave ausente de uma tabela = não coberta por aquele contrato. O app não
# a oferece na seleção. Ausência é regra de negócio, não esquecimento.
# ---------------------------------------------------------------------------

# Tabela comum a seis órgãos (itens a, d, i, j, k da Nota Técnica)
_PADRAO = {
    "Esquilo AS350": 9900.00,
    "Dauphin N2 (PP-EPO)": 16500.00,
    "Dauphin N3 (PR-DTG)": 16500.00,
    "King Air C90 (PR/PT-OSO)": 13750.00,
    "King Air B200 (PTWGS)": 13750.00,
    "King Air B300 (PP-EJO)": 13750.00,
    "King Air B350 (PR-XAA)": 13750.00,
    "Citation Bravo": 31900.00,
}

# Item (c) — SEAPA (nomenclatura por designação: BE9L, BE20, BE30, C550)
_SEAPA = {
    "Esquilo AS350": 11307.82,
    "Dauphin N2 (PP-EPO)": 29440.91,
    "Dauphin N3 (PR-DTG)": 29440.91,
    "King Air C90 (PR/PT-OSO)": 9055.37,
    "King Air B200 (PTWGS)": 12563.06,
    "King Air B300 (PP-EJO)": 15729.80,
    "King Air B350 (PR-XAA)": 15729.80,
    "Citation Bravo": 21276.38,
}

# Item (e) — SES 2 / Sistema Estadual de Doação e Transplantes (MG Transplantes)
_SES2 = {
    "Esquilo AS350": 11044.86,
    "Dauphin N2 (PP-EPO)": 27788.01,
    "Dauphin N3 (PR-DTG)": 27788.01,
    "King Air C90 (PR/PT-OSO)": 7859.79,
    "King Air B200 (PTWGS)": 11621.02,
    "King Air B300 (PP-EJO)": 14135.34,
    "King Air B350 (PR-XAA)": 14135.34,
    "Citation Bravo": 20644.58,
}

# Item (h) — GMG/PMMG, Tabela 13A (coluna "Valor operacional corrigido")
_GMG_13A = {
    "Esquilo AS350": 10216.36,
    "Dauphin N2 (PP-EPO)": 27090.64,
    "Dauphin N3 (PR-DTG)": 27090.64,
    "King Air C90 (PR/PT-OSO)": 7162.42,
    "King Air B200 (PTWGS)": 10923.65,
    "King Air B300 (PP-EJO)": 13437.97,
    "King Air B350 (PR-XAA)": 13437.97,
    "Citation Bravo": 19947.21,
}

# Item (l) — Prefeitura de Belo Horizonte (somente King Air)
_PBH = {
    "King Air C90 (PR/PT-OSO)": 9055.37,
    "King Air B200 (PTWGS)": 12563.06,
    "King Air B300 (PP-EJO)": 15729.80,
    "King Air B350 (PR-XAA)": 15729.80,
}

# Item (m) — Município de Uberlândia (somente Esquilo)
_UBERLANDIA = {
    "Esquilo AS350": 9900.00,
}

# Item (n) — CBM/PMMG/IPSM. O único jato previsto era o Citation VII (vendido),
# portanto o contrato ficou sem cobertura de jato.
_CBM_IPSM = {
    "Esquilo AS350": 8000.00,
    "Dauphin N2 (PP-EPO)": 14000.00,
    "Dauphin N3 (PR-DTG)": 14000.00,
    "King Air C90 (PR/PT-OSO)": 8000.00,
    "King Air B200 (PTWGS)": 9000.00,
    "King Air B300 (PP-EJO)": 12000.00,
    "King Air B350 (PR-XAA)": 12000.00,  # CONFERIR: a NT cita apenas "B300"
}

# ---------------------------------------------------------------------------
# ÓRGÃOS / CONTRATOS
# ---------------------------------------------------------------------------
CONTRATOS = {
    "TJM MG — Tribunal de Justiça Militar (TDCO)": {
        "sei": "1250.01.0022078/2024-91",
        "vigencia": "09/03/2030",
        "item_nt": "a",
        "precos": _PADRAO,
    },
    "TJMG — Tribunal de Justiça de MG (Convênio)": {
        "sei": "1250.01.0021166/2024-77",
        "vigencia": "29/04/2030",
        "item_nt": "i",
        "precos": _PADRAO,
    },
    "SES — Saúde em geral (TDCO SES 1)": {
        "sei": "1320.01.0114654/2023-89",
        "vigencia": "30/12/2026",
        "item_nt": "d",
        "precos": _PADRAO,
    },
    "CEMIG (Convênio)": {
        "sei": "1250.01.0000588/2025-64",
        "vigencia": "20/05/2030",
        "item_nt": "j",
        "precos": _PADRAO,
    },
    "COPASA (Convênio)": {
        "sei": "1250.01.0000423/2025-57",
        "vigencia": "15/07/2030",
        "item_nt": "k",
        "precos": _PADRAO,
    },
    "Uberlândia — Sec. Municipal de Saúde": {
        "sei": "1630.01.0001479/2024-38",
        "vigencia": "21/02/2030",
        "item_nt": "m",
        "precos": _UBERLANDIA,
        "observacao": "Convênio cobre exclusivamente o Esquilo AS350.",
    },
    "SEAPA — Secretaria de Agricultura": {
        "sei": "1250.01.0004203/2020-56",
        "vigencia": "19/10/2026",
        "item_nt": "c",
        "precos": _SEAPA,
    },
    "SES 2 — MG Transplantes (TDCO)": {
        "sei": "1250.01.0022846/2025-13",
        "vigencia": "23/05/2031",
        "item_nt": "e",
        "precos": _SES2,
    },
    "GMG/PMMG — Gestão da frota (Tabela 13A)": {
        "sei": "1070.01.0003858/2025-93",
        "vigencia": "30/06/2031",
        "item_nt": "h",
        "precos": _GMG_13A,
        "observacao": "Tabela 13A, coluna já corrigida pelo aumento do combustível.",
    },
    "PBH — Prefeitura de Belo Horizonte": {
        "sei": "1250.01.0000110/2026-66",
        "vigencia": "19/05/2030",
        "item_nt": "l",
        "precos": _PBH,
        "observacao": "Convênio cobre exclusivamente aeronaves King Air.",
    },
    "CBM/PMMG/IPSM (Convênio)": {
        "sei": "2120.01.0004933/2022-69",
        "vigencia": "Não informada na Nota Técnica",
        "item_nt": "n",
        "precos": _CBM_IPSM,
        "observacao": "Sem cobertura de jato: o único previsto era o Citation VII, vendido.",
    },
}

REFERENCIA_NOTA_TECNICA = (
    "Nota Técnica nº 21/PMMG/COMAVE 4 - TDCO/CONV./2026 · "
    "SEI nº 144797834 · atualizada em 17/07/2026"
)
