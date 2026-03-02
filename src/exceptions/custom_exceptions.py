"""Módulo de exceções customizadas."""


class ConfigurationError(Exception):
    """Erro para falhas de configuração do projeto."""
    def __init__(self, message: str):
        super().__init__(f"Configuration Error: {message}")


class DataIngestionError(Exception):
    """Erro para falhas na ingestão de dados."""
    def __init__(self, message: str):
        super().__init__(f"Data Ingestion Error: {message}")


class DataValidationError(Exception):
    """Erro para inconsistências de validação de dados."""
    def __init__(self, message: str):
        super().__init__(f"Data Validation Error: {message}")


class ModelTrainingError(Exception):
    """Erro para falhas de treinamento de modelos."""
    def __init__(self, message: str):
        super().__init__(f"Model Training Error: {message}")