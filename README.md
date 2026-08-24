# Planejador de Missões Aéreas - DTA

Roteirizador point-to-point multipernas para estimativa de tempo e custo de missões aéreas.

## Arquivos

| Arquivo | Papel |
|---|---|
| `app.py` | Interface Streamlit (três abas: cálculo DTA, cálculo COMAVE, consulta) |
| `dados.py` | Base estática **da DTA**: aeródromos, frota, coordenadas de emergência |
| `regras.py` | Regras de negócio puras da DTA (distância, velocidade, restrições) |
| `dados_comave.py` | Tabelas de custo **do COMAVE** por órgão/contrato (Nota Técnica nº 21) |
| `regras_comave.py` | Regras de tempo de solo e trecho tabelado do COMAVE |
| `aba_comave.py` | Interface da aba COMAVE |
| `gerar_coordenadas.py` | Script auxiliar, rodado uma vez para gerar o JSON de coordenadas |
| `tests/test_regras.py` | Suíte de regressão da DTA (pytest) |
| `tests/test_comave.py` | Suíte de regressão do COMAVE: 7 tabelas conferidas valor a valor |
| `RELACAO_CIDADES_MG_ESQUILO.csv` | Catálogo de áreas livres (colunas: `CIDADE`, `LATITUDE`, `LONGITUDE`) |
| `coordenadas_aerodromos.json` | Gerado pelo script acima — **versionar no repositório** |

## Instalação

```bash
pip install -r requirements.txt
python gerar_coordenadas.py     # roda uma vez, gera o JSON; commitar o resultado
streamlit run app.py
```

## Testes

```bash
pip install pytest
pytest -v
```

## Manutenção

- **Novo aeródromo:** adicionar em `dados.AEROPORTOS` e rodar `gerar_coordenadas.py` de novo.
- **Novo valor de hora de voo:** alterar em `dados.FROTA`.
- **Mudança de regra operacional:** alterar em `regras.py` e ajustar o teste correspondente.
- Se o app avisar que há aeródromos sem coordenada, rodar `gerar_coordenadas.py`. Rota
  envolvendo aeródromo sem coordenada **não é calculada** — o app informa em vez de estimar errado.

## Separação DTA x COMAVE

São **dois clientes distintos com tabelas de custo próprias**. A aba DTA usa
exclusivamente `dados.py`/`regras.py`; a aba COMAVE usa exclusivamente
`dados_comave.py`/`regras_comave.py`. Coincidência numérica entre as duas
nunca é motivo para unificar. Compartilham apenas geografia (aeródromos e
coordenadas) e as validações de pista/ANAC, que são fatos operacionais.

## Premissas do cálculo — DTA

- Distância ortodrômica (círculo máximo) entre coordenadas, em milhas náuticas (NM).
- Tempo de decolagem a pouso. Táxi, espera e vetoração **não** entram; são informados à parte.
- King Air B200: se o tempo na velocidade base atingir 1 h, a perna inteira passa para 225 KT.
  A regra é descontínua por definição da tabela do operador (200 NM custa menos que 199 NM).
- BH x Confins (SBBH x SBCF): tempo tabelado de **10 minutos**, faturado por esse tempo.
  É a única exceção ao cálculo por distância na aba DTA.
- Aeródromo com restrição da ANAC bloqueia o **custo total** da missão para aeronaves de asa
  fixa; a tabela é exibida para que o planejamento seja refeito. Helicópteros são isentos.

## Premissas do cálculo — COMAVE

- Fonte: Nota Técnica nº 21/PMMG/COMAVE 4 - TDCO/CONV./2026 (SEI nº 144797834, 17/07/2026).
- O valor da hora depende do **órgão/contrato selecionado**. Aeronave ausente de uma tabela
  não é oferecida naquele contrato (PBH só King Air, Uberlândia só Esquilo, CBM sem jato).
- Acréscimo de solo: **15 min por aeroporto** (origem e destino), **25 min em capital**,
  **5 min por perna** para helicóptero. Entra no tempo exibido e **não é faturado**.
- BH x Confins: tempo tabelado de **15 minutos**, faturado integralmente.
- O Citation VII (C650, PTMGS) foi vendido e não consta de nenhuma tabela.

## Pendências de confirmação (COMAVE)

1. **SBBH e SBCF como capital?** Hoje recebem 15 min de solo, não 25, em pernas que não
   sejam o par BH x Confins. Para mudar: incluir os dois em `CAPITAIS_ICAO`
   (`regras_comave.py`). Há teste cobrindo a decisão atual.
2. **Helicóptero: 5 min por perna ou 5 min por ponta?** Implementado como 5 min por perna.
   Para mudar: `MIN_SOLO_HELI` em `regras_comave.py`.
3. **CBM/PMMG/IPSM:** a Nota Técnica cita apenas "King Air B300" a R$ 12.000. O B350
   (PR-XAA) foi mapeado no mesmo valor. Confirmar com o contrato.
4. **Cessna 210 (PP-HAC):** consta de quatro tabelas do COMAVE, mas não foi incluído por
   falta de velocidade de cruzeiro e capacidade oficiais.
