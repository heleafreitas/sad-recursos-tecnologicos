"""
Serviço principal de recomendação
Integra as três funções de análise de dados
"""
from config import Config
from services.classificacao import ClassificadorRecursos
from services.associacao import AnalisadorAssociacao
from services.agrupamento import AgrupadorSimilaridade

class SistemaRecomendacao:
    """
    Integra classificação, associação e agrupamento para gerar recomendações
    """
    
    def __init__(self, respostas, recursos):
        self.respostas = respostas
        self.recursos = recursos
        
        # Inicializa os três motores de análise
        self.classificador = ClassificadorRecursos(respostas)
        self.associador = AnalisadorAssociacao(respostas)
        self.agrupador = AgrupadorSimilaridade(respostas)
    
    def gerar_recomendacoes(self):
        """
        Pipeline completo de recomendação
        
        Returns:
            dict: Contém ranking e análises estatísticas
        """
        # ETAPA 1: Classificação - Filtra recursos elegíveis
        recursos_elegiveis = self.classificador.filtrar_recursos_elegiveis(
            self.recursos
        )
        
        if not recursos_elegiveis:
            return {
                'ranking': [],
                'analises': {
                    'totalRecursos': len(self.recursos),
                    'recursosElegiveis': 0,
                    'taxaFiltragem': 100.0,
                    'mensagem': 'Nenhum recurso atende aos critérios especificados'
                }
            }
        
        # ETAPA 2: Score individual para cada recurso elegível
        recursos_com_score = []
        
        for recurso in recursos_elegiveis:
            # Calcula score base (média ponderada das características)
            score_base = self._calcular_score_base(recurso)
            
            # ETAPA 3: Análise de Associação
            score_associacao = self.associador.calcular_score_associacao(recurso)
            
            # ETAPA 4: Agrupamento por Similaridade
            score_similaridade = self.agrupador.calcular_similaridade(recurso)
            
            # ETAPA 5: Score final ponderado
            score_final = (
                score_base * Config.PESO_SCORE_BASE +
                score_associacao * Config.PESO_ASSOCIACAO +
                score_similaridade * Config.PESO_SIMILARIDADE
            )
            
            # Obtem regras ativadas para explicabilidade
            regras_ativadas = self.associador.obter_regras_ativadas(recurso)
            distancias = self.agrupador.obter_distancias_detalhadas(recurso)
            
            recursos_com_score.append({
                'recurso': recurso,
                'scoreBase': round(score_base, 4),
                'scoreAssociacao': round(score_associacao, 4),
                'scoreSimilaridade': round(score_similaridade, 4),
                'scoreFinal': round(score_final, 4),
                'regrasAtivadas': regras_ativadas,
                'distancias': distancias
            })
        
        # ETAPA 6: Ordena por score final
        recursos_com_score.sort(key=lambda x: x['scoreFinal'], reverse=True)
        
        # ETAPA 7: Retorna top N recomendações
        ranking = recursos_com_score[:Config.NUM_RECOMENDACOES]
        
        # ETAPA 8: Análises estatísticas
        analises = self._gerar_analises(recursos_com_score, len(self.recursos))
        
        return {
            'ranking': [self._formatar_resultado(r) for r in ranking],
            'analises': analises
        }
    
    def _calcular_score_base(self, recurso):
        """
        Calcula score base baseado nas características intrínsecas
        
        Returns:
            float: Score base [0-1]
        """
        pesos = Config.PESOS_CARACTERISTICAS
        
        score = (
            recurso.facilidadeUso * pesos['facilidadeUso'] +
            recurso.engajamentoPotencial * pesos['engajamentoPotencial'] +
            recurso.adaptabilidadePedagogica * pesos['adaptabilidadePedagogica'] +
            recurso.requisitosInfraestrutura * pesos['requisitosInfraestrutura'] +
            recurso.custoAcessibilidade * pesos['custoAcessibilidade']
        )
        
        return score
    
    def _gerar_analises(self, recursos_com_score, total_recursos):
        """
        Gera estatísticas sobre o processo de recomendação
        
        Returns:
            dict: Análises estatísticas
        """
        if not recursos_com_score:
            return {}
        
        scores_finais = [r['scoreFinal'] for r in recursos_com_score]
        scores_associacao = [r['scoreAssociacao'] for r in recursos_com_score]
        scores_similaridade = [r['scoreSimilaridade'] for r in recursos_com_score]
        
        # Determina qual critério foi mais importante
        media_associacao = sum(scores_associacao) / len(scores_associacao)
        media_similaridade = sum(scores_similaridade) / len(scores_similaridade)
        
        criterio_predominante = (
            'Associação' if media_associacao > media_similaridade 
            else 'Similaridade'
        )
        
        return {
            'totalRecursos': total_recursos,
            'recursosElegiveis': len(recursos_com_score),
            'taxaFiltragem': round(
                ((total_recursos - len(recursos_com_score)) / total_recursos) * 100, 
                1
            ),
            'mediaScoreFinal': round(sum(scores_finais) / len(scores_finais), 3),
            'medianaScoreFinal': round(
                sorted(scores_finais)[len(scores_finais) // 2], 
                3
            ),
            'principalCriterio': criterio_predominante,
            'mediaAssociacao': round(media_associacao, 3),
            'mediaSimilaridade': round(media_similaridade, 3)
        }
    
    def _formatar_resultado(self, resultado):
        """
        Formata resultado para envio ao frontend
        
        Returns:
            dict: Resultado formatado
        """
        recurso = resultado['recurso']
        
        return {
            'id': recurso.id,
            'nome': recurso.nome,
            'area': recurso.area,
            'categoria': recurso.categoria,
            'descricao': recurso.descricao,
            'scoreBase': resultado['scoreBase'],
            'scoreAssociacao': resultado['scoreAssociacao'],
            'scoreSimilaridade': resultado['scoreSimilaridade'],
            'scoreFinal': resultado['scoreFinal'],
            'regrasAtivadas': resultado['regrasAtivadas'],
            'distancias': resultado['distancias'],
            'caracteristicas': {
                'facilidadeUso': recurso.facilidadeUso,
                'engajamentoPotencial': recurso.engajamentoPotencial,
                'adaptabilidadePedagogica': recurso.adaptabilidadePedagogica,
                'requisitosInfraestrutura': recurso.requisitosInfraestrutura,
                'custoAcessibilidade': recurso.custoAcessibilidade
            },
            'referencias': recurso.referencias
        }