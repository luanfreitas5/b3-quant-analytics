"""Dashboard Streamlit (esqueleto)."""

from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="B3 Quant Analytics", layout="wide")
st.title("B3 Quant Analytics Dashboard")

metrics_path = Path("reports/metrics/model_metrics.json")
features_path = Path("data/processed/features.csv")

if metrics_path.exists():
    st.subheader("Métricas do Modelo")
    st.json(metrics_path.read_text(encoding="utf-8"))
else:
    st.info("Execute o pipeline para gerar métricas.")

if features_path.exists():
    st.subheader("Prévia de Features")
    st.dataframe(pd.read_csv(features_path).head(50), use_container_width=True)
