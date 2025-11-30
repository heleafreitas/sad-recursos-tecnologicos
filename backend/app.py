"""
API Flask para o Sistema de Apoio à Decisão
Versão 2.0 com Classificação, Agrupamento e Regressão
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models.recursos import RecursosRepository
from models.questionario import RespostasQuestionario
from services.recomendacao import SistemaRecomendacao
import logging

# Configurar logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format=Config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Inicializa repositório de recursos
recursos_repo = RecursosRepository()

@app.route('/api/recursos', methods=['GET'])
def listar_recursos():
    """
    GET /api/recursos
    Retorna lista de todos os recursos disponíveis
    """
    try:
        recursos = recursos_repo.obter_todos()
        logger.info(f"Listando {len(recursos)} recursos")
        return jsonify({
            'success': True,
            'data': [r.to_dict() for r in recursos]
        })
    except Exception as e:
        logger.error(f"Erro ao listar recursos: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recomendacoes', methods=['POST'])
def gerar_recomendacoes():
    """
    POST /api/recomendacoes
    Gera recomendações baseado nas respostas do questionário
    """
    try:
        # Valida request
        dados = request.get_json()
        if not dados:
            logger.warning("Requisição sem dados recebida")
            return jsonify({
                'success': False,
                'error': 'Dados do questionário não fornecidos'
            }), 400
        
        logger.info(f"Gerando recomendações para disciplina: {dados.get('disciplina')}")
        
        # Cria objeto de respostas
        respostas = RespostasQuestionario(dados)
        
        # Obtém recursos
        recursos = recursos_repo.obter_todos()
        
        # Gera recomendações usando o novo sistema integrado
        sistema = SistemaRecomendacao(respostas, recursos)
        resultado = sistema.gerar_recomendacoes()

        logger.info(f"Recomendações geradas com sucesso. Total: {len(resultado['ranking'])}")
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except ValueError as e:
        logger.error(f"Erro de validação: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro de validação: {str(e)}'
        }), 400
    except Exception as e:
        logger.error(f"Erro interno: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/api/metodologia', methods=['GET'])
def obter_metodologia():
    """
    GET /api/metodologia
    Retorna informações sobre a metodologia de análise
    
    Response:
        {
            "success": true,
            "data": {
                "funcoes": [
                    {
                        "nome": "Classificação (Decision Tree)",
                        "descricao": "...",
                        "peso": "Filtro binário"
                    },
                    {
                        "nome": "Agrupamento (K-Means)",
                        "descricao": "...",
                        "peso": "Categorização"
                    },
                    {
                        "nome": "Regressão Linear",
                        "descricao": "...",
                        "peso": "100% (define pesos)"
                    }
                ],
                "formula_score_final": "Score = Σ(característica × peso_regressão)",
                "clusters": {...},
                "referencias": [...]
            }
        }
    """
    return jsonify({
        'success': True,
        'data': {
            'funcoes': [
                {
                    'nome': 'Classificação (Decision Tree)',
                    'descricao': 'Filtra recursos incompatíveis usando árvore de decisão com 6 regras de negócio',
                    'biblioteca': 'Scikit-learn DecisionTreeClassifier',
                    'peso': 'Filtro binário (elegível/não elegível)'
                },
                {
                    'nome': 'Agrupamento (K-Means)',
                    'descricao': 'Agrupa recursos elegíveis em clusters semânticos com nomes descritivos',
                    'biblioteca': 'Scikit-learn KMeans',
                    'peso': 'Categorização para organização',
                    'clusters': {
                        '0': 'Ferramentas Iniciante-Friendly',
                        '1': 'Ferramentas Avançadas',
                        '2': 'Ferramentas Colaborativas'
                    }
                },
                {
                    'nome': 'Regressão Linear',
                    'descricao': 'Calcula pesos ótimos para as 5 características principais',
                    'biblioteca': 'Scikit-learn LinearRegression',
                    'peso': '100% (define todos os pesos do score final)',
                    'variaveis': [
                        'facilidadeUso',
                        'engajamentoPotencial',
                        'adaptabilidadePedagogica',
                        'requisitosInfraestrutura',
                        'custoAcessibilidade'
                    ]
                }
            ],
            'formula_score_final': 'Score = (facilidadeUso × w1) + (engajamentoPotencial × w2) + (adaptabilidadePedagogica × w3) + (requisitosInfraestrutura × w4) + (custoAcessibilidade × w5)',
            'notas': [
                'Os pesos (w1-w5) são calculados dinamicamente pela regressão',
                'A regressão normaliza os coeficientes para somar 1.0',
                'Os clusters são nomeados automaticamente baseado nas características',
                'A classificação garante que apenas recursos elegíveis sejam recomendados'
            ],
            'fluxo_pipeline': [
                '1. Regressão Linear treina para obter pesos ótimos',
                '2. Decision Tree filtra recursos elegíveis (critérios de negócio)',
                '3. K-Means agrupa recursos em clusters semânticos',
                '4. Score final calcula compatibilidade com pesos da regressão',
                '5. Ranking ordena recursos por score final (descendente)'
            ],
            'referencias': [
                'Breiman, L., et al. (1984). Classification and Regression Trees',
                'MacQueen, J. (1967). Some methods for classification and analysis',
                'Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules',
                'Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python'
            ]
        }
    })

@app.route('/api/diagnostico', methods=['POST'])
def obter_diagnostico():
    """
    POST /api/diagnostico
    Retorna informações detalhadas sobre o processo de recomendação
    (útil para debug e análise)
    """
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({
                'success': False,
                'error': 'Dados não fornecidos'
            }), 400
        
        respostas = RespostasQuestionario(dados)
        recursos = recursos_repo.obter_todos()
        sistema = SistemaRecomendacao(respostas, recursos)
        
        # Executa apenas classificação para diagnóstico
        recursos_elegiveis = sistema.classificador.filtrar_recursos_elegiveis(recursos)
        importancia_features = sistema.classificador.obter_importancia_features()
        
        # Executa regressão para diagnóstico
        pesos = sistema.regressor.treinar_regressao(recursos)
        metricas_regressao = sistema.regressor.obter_metricas()
        
        logger.info("Diagnóstico gerado com sucesso")
        
        return jsonify({
            'success': True,
            'data': {
                'classificacao': {
                    'total_elegivel': len(recursos_elegiveis),
                    'total_inelegivel': len(recursos) - len(recursos_elegiveis),
                    'taxa_elegibilidade': len(recursos_elegiveis) / len(recursos),
                    'importancia_features': importancia_features
                },
                'regressao': metricas_regressao,
                'recursos': [r.to_dict() for r in recursos]
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao gerar diagnóstico: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Sistema de Apoio à Decisão - API v2.0',
        'features': [
            'Classificação (Decision Tree)',
            'Agrupamento (K-Means)',
            'Regressão Linear'
        ]
    })

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=5000, host='0.0.0.0')