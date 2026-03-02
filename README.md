# B3 Quant Analytics: Risk & Return Analysis Pipeline

Projeto completo de Ciência de Dados em Python para análise quantitativa de ativos da B3, com pipeline automatizado de ingestão, armazenamento relacional, engenharia de features de risco e modelagem preditiva de retorno.

## Contexto de negócio

Gestores e analistas de investimentos precisam avaliar risco e retorno de ativos em escala, com métricas robustas, consistência de dados e reprodutibilidade. Este projeto simula uma plataforma de analytics quantitativo para apoiar decisão de alocação.

## Palavras-chave e competências

- Data Engineering para Finanças
- Análise Quantitativa
- Pandas Avançado (groupby, merges, otimização de memória)
- SQL Avançado (CTE, window functions)
- Machine Learning com scikit-learn
- Estatística aplicada com statsmodels
- Engenharia de software para DS (logging, testes, CLI, Docker, CI)

## Problema e objetivos

### Problema

Consolidar dados de mercado de múltiplos ativos da B3, calcular métricas de risco e prever retorno diário futuro de forma reproduzível.

### Objetivos

1. Ingerir dados de API (Yahoo Finance).
2. Persistir dados em banco relacional (SQLite, facilmente adaptável para PostgreSQL).
3. Calcular retornos, volatilidade anualizada, Sharpe Ratio e VaR histórico.
4. Treinar modelo para previsão de retorno `t+1`.
5. Gerar artefatos analíticos e métricas para suporte à decisão.

## Dataset / API

- **Fonte**: Yahoo Finance (`yfinance`)
- **Ativos padrão**: PETR4.SA, VALE3.SA, ITUB4.SA, BBDC4.SA
- **Periodicidade**: diária (`1d`)
- **Atributos principais**: `date`, `ticker`, `open`, `high`, `low`, `close`, `adj_close`, `volume`

## Arquitetura do projeto

```text
b3-quant-analytics/
├── configs/
├── data/
│   ├── raw/
│   ├── external/
│   ├── interim/
│   └── processed/
├── docs/
├── notebooks/
├── reports/
│   ├── figures/
│   └── metrics/
├── scripts/
├── src/
│   ├── main.py
│   ├── ingestion/
│   ├── processing/
│   ├── features/
│   ├── models/
│   ├── pipelines/
│   ├── utils/
│   └── exceptions/
└── tests/
```

## Tecnologias e bibliotecas

- Python 3.8+
- pandas, numpy, statsmodels
- scikit-learn
- yfinance
- matplotlib, seaborn
- sqlite3
- tqdm
- python-dotenv
- pytest
- black

## Como executar

### 1) Preparar ambiente

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
copy .env.example .env
```

### 2) Rodar pipeline completo

```bash
python src/main.py run
```

### 2.1) Rodar pipeline por inferência

```bash
python src/main.py infer --model-path .\models\return_model.joblib --input .\data\processed\features.csv
```

### 3) Rodar testes

```bash
pytest
```

### 4) Formatar código

```bash
black src tests scripts
```

## Principais saídas

- `data/processed/features.csv`: dataset de features
- `models/return_model.joblib`: modelo treinado
- `models/model_metadata.json`: metadados do modelo
- `reports/figures/correlation_heatmap.png`: mapa de correlação
- `reports/metrics/model_metrics.json`: métricas de avaliação
- `logs/*.log`: logs versionados por data/hora e nível

## Próximos passos

1. Suportar PostgreSQL em produção via `SQLAlchemy`.
2. Incluir backtesting com métricas de estratégia (CAGR, max drawdown).
3. Criar dashboard interativo (Streamlit).
4. Adicionar monitoramento de drift de distribuição.
5. Evoluir para previsão multihorizonte e modelos de séries temporais.

## Licença

Este projeto está licenciado sob a licença MIT.
