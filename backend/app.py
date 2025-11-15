"""
API Flask para o Sistema de Apoio à Decisão
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models.recursos import RecursosRepository
from models.questionario import RespostasQuestionario
from services.recomendacao import SistemaRecomendacao

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
        return jsonify({
            'success': True,
            'data': [r.to_dict() for r in recursos]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recomendacoes', methods=['POST'])
def gerar_recomendacoes():
    """
    POST /api/recomendacoes
    Recebe respostas do questionário e retorna ranking de recomendações
    
    Body:
        {
            "disciplina": "Matemática",
            "familiaridadeTech": 0.6,
            "estiloEnsino": "investigativo",
            ...
        }
    
    Response:
        {
            "success": true,
            "data": {
                "ranking": [...],
                "analises": {...}
            }
        }
    """
    try:
        # Valida request
        dados = request.get_json()
        if not dados:
            return jsonify({
                'success': False,
                'error': 'Dados do questionário não fornecidos'
            }), 400
        
        # Cria objeto de respostas
        respostas = RespostasQuestionario(dados)
        
        # Obtém recursos
        recursos = recursos_repo.obter_todos()
        
        # Gera recomendações
        sistema = SistemaRecomendacao(respostas, recursos)
        resultado = sistema.gerar_recomendacoes()
        
        return jsonify({
            'success': True,
            'data': resultado
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Erro de validação: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/api/metodologia', methods=['GET'])
def obter_metodologia():
    """
    GET /api/metodologia
    Retorna informações sobre a metodologia de análise
    """
    return jsonify({
        'success': True,
        'data': {
            'funcoes': [
                {
                    'nome': 'Classificação (Decision Tree)',
                    'descricao': 'Filtra recursos incompatíveis usando árvore de decisão com 6 regras',
                    'biblioteca': 'Lógica de negócio baseada em Scikit-learn',
                    'peso': 'Filtro binário (elegível/não elegível)'
                },
                {
                    'nome': 'Análise de Associação',
                    'descricao': 'Identifica padrões entre contexto do professor e recursos adequados',
                    'biblioteca': 'NumPy para cálculos vetorizados',
                    'peso': f'{int(Config.PESO_ASSOCIACAO * 100)}% do score final'
                },
                {
                    'nome': 'Agrupamento por Similaridade',
                    'descricao': 'Calcula distância euclidiana entre perfil e recursos',
                    'biblioteca': 'NumPy e Scikit-learn (MinMaxScaler)',
                    'peso': f'{int(Config.PESO_SIMILARIDADE * 100)}% do score final'
                }
            ],
            'formula_score_final': 'Score = (Base × 0.30) + (Associação × 0.35) + (Similaridade × 0.35)',
            'referencias': [
                'Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules',
                'MacQueen, J. (1967). Some methods for classification and analysis',
                'Breiman, L., et al. (1984). Classification and Regression Trees'
            ]
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Sistema de Apoio à Decisão - API'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)