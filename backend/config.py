"""
Configurações do Sistema de Apoio à Decisão
"""

class Config:
    # Configurações Flask
    DEBUG = True
    SECRET_KEY = 'dev-secret-key-change-in-production'
    
    # Pesos para cálculo do score final
    PESO_SCORE_BASE = 0.30
    PESO_ASSOCIACAO = 0.35
    PESO_SIMILARIDADE = 0.35
    
    # Pesos das características intrínsecas
    PESOS_CARACTERISTICAS = {
        'facilidadeUso': 0.20,
        'engajamentoPotencial': 0.25,
        'adaptabilidadePedagogica': 0.20,
        'requisitosInfraestrutura': 0.15,
        'custoAcessibilidade': 0.20
    }
    
    # Limites para filtragem
    LIMIAR_FAMILIARIDADE_BAIXA = 0.5
    LIMIAR_FACILIDADE_MINIMA = 0.7
    LIMIAR_CONECTIVIDADE_OFFLINE = 0.4
    
    # Número de recomendações a retornar
    NUM_RECOMENDACOES = 5