# Arquitetura

## Visão Geral

O projeto segue uma arquitetura modular em camadas:

1. **Ingestão**: coleta de dados históricos via Yahoo Finance e persistência em SQLite.
2. **Processamento**: limpeza, validação e transformação em retornos.
3. **Features**: cálculo de volatilidade, Sharpe Ratio e VaR.
4. **Modelagem**: treino de RandomForest para previsão de retorno t+1.
5. **Pipelines**: orquestração ponta a ponta com geração de artefatos e relatórios.

## Princípios

- Funções com responsabilidade única
- Baixo acoplamento
- Tratamento explícito de erros
- Reprodutibilidade via `.env`, `requirements.txt` e `pytest`
