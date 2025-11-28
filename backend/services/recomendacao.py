"""
SERVIÇO PRINCIPAL DE RECOMENDAÇÃO - Integra as 3 funções
"""
from services.classificacao import ClassificadorRecursos
from services.agrupamento import AgrupadorSimilaridade
from services.regressao import RegressorPesos


class SistemaRecomendacao:
    """Integra classificação, agrupamento e regressão para gerar recomendações"""
    
    def __init__(self, respostas, recursos):
        self.respostas = respostas
        self.recursos = recursos
        
        # Inicializa os três motores
        self.classificador = ClassificadorRecursos(respostas)
        self.agrupador = AgrupadorSimilaridade(respostas)
        self.regressor = RegressorPesos()
    
    def gerar_recomendacoes(self):
        """Pipeline completo de recomendação"""
        # ETAPA 1: Treina regressão para obter pesos
        pesos = self.regressor.treinar_regressao(self.recursos)
        
        # ETAPA 2: Classificação - Filtra recursos elegíveis
        recursos_elegiveis = self.classificador.filtrar_recursos_elegiveis(self.recursos)
        
        if not recursos_elegiveis:
            return {
                'ranking': [],
                'analises': {
                    'totalRecursos': len(self.recursos),
                    'recursosElegiveis': 0,
                    'pesos_regressao': pesos,
                    'metricas_regressao': self.regressor.obter_metricas()
                }
            }
        
        # ETAPA 3: Agrupamento - Agrupa recursos elegíveis
        clusters_info = self.agrupador.agrupar_recursos(recursos_elegiveis, n_clusters=3)
        self.agrupador.nomes_clusters = self._nomear_clusters(clusters_info)
        
        # ETAPA 4: Calcula score final com pesos da regressão
        recursos_com_score = []
        
        for recurso in recursos_elegiveis:
            score_final = (
                recurso.facilidadeUso * pesos['facilidadeUso'] +
                recurso.engajamentoPotencial * pesos['engajamentoPotencial'] +
                recurso.adaptabilidadePedagogica * pesos['adaptabilidadePedagogica'] +
                recurso.requisitosInfraestrutura * pesos['requisitosInfraestrutura'] +
                recurso.custoAcessibilidade * pesos['custoAcessibilidade']
            )
            
            # Obter cluster do recurso
            idx_recurso = recursos_elegiveis.index(recurso) if recurso in recursos_elegiveis else -1
            cluster_id = self.agrupador.labels_recursos[idx_recurso] if idx_recurso >= 0 else 0
            
            distancias = self.agrupador.obter_distancias_detalhadas(recurso)
            
            recursos_com_score.append({
                'recurso': recurso,
                'scoreFinal': round(score_final, 4),
                'cluster_id': int(cluster_id),
                'distancias': distancias
            })
        
        # ETAPA 5: Ordena por score final
        recursos_com_score.sort(key=lambda x: x['scoreFinal'], reverse=True)
        
        # ETAPA 6: Retorna top 10
        ranking = recursos_com_score[:10]
        
        analises = self._gerar_analises(recursos_com_score, len(self.recursos), pesos)
        
        return {
            'ranking': [self._formatar_resultado(r) for r in ranking],
            'analises': analises
        }
    
    def _nomear_clusters(self, clusters_info):
        """Atribui nomes descritivos aos clusters"""
        nomes = {}
        
        cluster_names = {
            0: "Ferramentas Iniciante-Friendly",
            1: "Ferramentas Avançadas",
            2: "Ferramentas Colaborativas"
        }
        
        for label in clusters_info['clusters'].keys():
            nomes[label] = cluster_names.get(label, f"Cluster {label}")
        
        return nomes
    
    def _gerar_analises(self, recursos_com_score, total_recursos, pesos):
        """Gera estatísticas sobre o processo"""
        if not recursos_com_score:
            return {}
        
        scores_finais = [r['scoreFinal'] for r in recursos_com_score]
        
        return {
            'totalRecursos': total_recursos,
            'recursosElegiveis': len(recursos_com_score),
            'taxaFiltragem': round(
                ((total_recursos - len(recursos_com_score)) / total_recursos) * 100, 1
            ),
            'mediaScoreFinal': round(sum(scores_finais) / len(scores_finais), 3),
            'medianaScoreFinal': round(sorted(scores_finais)[len(scores_finais) // 2], 3),
            'pesos_regressao': pesos,
            'metricas_regressao': self.regressor.obter_metricas()
        }
    
    def _formatar_resultado(self, resultado):
        """Formata resultado para envio ao frontend"""
        recurso = resultado['recurso']
        
        return {
            'id': recurso.id,
            'nome': recurso.nome,
            'area': recurso.area,
            'categoria': recurso.categoria,
            'descricao': recurso.descricao,
            'scoreFinal': resultado['scoreFinal'],
            'cluster_id': resultado['cluster_id'],
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