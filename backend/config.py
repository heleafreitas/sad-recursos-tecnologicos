"""
Configurações do Sistema de Apoio à Decisão
"""
import os

class Config:
    """Configurações gerais da aplicação"""
    
    # Flask
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # CORS
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000']
    
    # Recomendações
    NUM_RECOMENDACOES = 50
    NUM_CLUSTERS = 6  # K-Means clustering
    
    # Pesos da Regressão (serão calculados dinamicamente)
    # Estes são valores padrão, mas serão substituídos pelos pesos da regressão
    PESOS_REGRESSAO_PADRAO = {
        'facilidadeUso': 0.22,
        'engajamentoPotencial': 0.18,
        'adaptabilidadePedagogica': 0.28,
        'requisitosInfraestrutura': 0.15,
        'custoAcessibilidade': 0.17
    }
    
    # Limites de features para classificação
    MIN_FACILIDADE = 0.7
    MIN_ENGAJAMENTO = 0.75
    MIN_ADAPTABILIDADE = 0.70
    
    # Limiares de conectividade
    LIMIAR_CONECTIVIDADE_BAIXA = 0.4
    LIMIAR_FAMILIARIDADE_BAIXA = 0.5
    
    # Limiares de engajamento e desempenho para análise de associação
    LIMIAR_ENGAJAMENTO_BAIXO = 0.5
    LIMIAR_DESEMPENHO_BAIXO = 0.5
    LIMIAR_TEMPO_LIMITADO = 0.5
    
    # Dados
    DADOS_DIR = os.path.join(os.path.dirname(__file__), 'data')
    RECURSOS_JSON = os.path.join(DADOS_DIR, 'recursos_base.json')
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Nomes dos Clusters para o Agrupamento
    CLUSTER_NAMES = {
        0: "Ferramentas Iniciante-Friendly",
        1: "Ferramentas Avançadas",
        2: "Ferramentas de Gamificação",
        3: "Ferramentas Colaborativas",
        4: "Ferramentas de Laboratório Virtual",
        5: "Ferramentas Multifuncionais"
    }
    
    # Máquina Learning
    ML_RANDOM_STATE = 42
    ML_CV_FOLDS = 5
    ML_TREE_MAX_DEPTH = 5
    ML_KMEANS_INIT = 'k-means++'
    ML_KMEANS_N_INIT = 10
    
    # Regressão
    REGRESSAO_TIPO = 'linear'  # Tipo de regressão: 'linear', 'ridge', 'lasso'
    REGRESSAO_TARGET = 'adaptabilidadePedagogica'  # Variável target