# Planejador de Missões Aéreas - DTA

Roteirizador point-to-point multipernas para estimativa de tempo e custo de missões aéreas.

## Arquivos

| Arquivo | Papel |
|---|---|
| `app.py` | Interface Streamlit (duas abas: cálculo de missão e consulta de aeródromos) |
| `dados.py` | Base estática: aeródromos, frota, coordenadas de emergência |
| `regras.py` | Regras de negócio puras (distância, velocidade, restrições) — sem Streamlit |
| `gerar_coordenadas.py` | Script auxiliar, rodado uma vez para gerar o JSON de coordenadas |
| `tests/test_regras.py` | Suíte de regressão (pytest) |
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

## Premissas do cálculo

- Distância ortodrômica (círculo máximo) entre coordenadas, em milhas náuticas (NM).
- Tempo de decolagem a pouso. Táxi, espera e vetoração **não** entram; são informados à parte.
- King Air B200: se o tempo na velocidade base atingir 1 h, a perna inteira passa para 225 KT.
  A regra é descontínua por definição da tabela do operador (200 NM custa menos que 199 NM).
- Aeródromo com restrição da ANAC bloqueia o **custo total** da missão para aeronaves de asa
  fixa; a tabela é exibida para que o planejamento seja refeito. Helicópteros são isentos.
