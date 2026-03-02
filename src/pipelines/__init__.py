"""Módulos de orquestração de pipelines."""

from pipelines.inference_pipeline import run_inference_pipeline
from pipelines.training_pipeline import run_training_pipeline

__all__ = ["run_training_pipeline", "run_inference_pipeline"]
