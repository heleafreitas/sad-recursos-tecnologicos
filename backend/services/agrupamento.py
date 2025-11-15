"""
FUNÇÃO 3: AGRUPAMENTO POR SIMILARIDADE (K-Means Adaptado)
Calcula distância euclidiana entre perfil do professor e recursos
Baseado em: Scikit-learn KMeans e distância euclidiana
Referência: MacQueen, J. (1967). Some methods for classification and analysis
"""
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class AgrupadorSimilaridade:
    """
    Implementa clustering adaptado para medir similaridade perfil-recurso
    """
    
    def __init__(self, respostas):
        self.respostas = respostas
        self.scaler = MinMaxScaler()
    
    def calcular_similaridade(self, recurso):
        """
        Calcula similaridade usando distância euclidiana normalizada
        
        Fórmula: Similaridade = 1 - (distância / distância_máxima)
        Onde distância = √Σ(perfil_i - recurso_i)²
        
        Returns:
            float: Score de similaridade [0-1]
        """
        # Vetor de características do professor (normalizado)
        vetor_professor = self._construir_vetor_professor()
        
        # Vetor de características do recurso (normalizado)
        vetor_recurso = self._construir_vetor_recurso(recurso)
        
        # Calcula distância euclidiana
        distancia = np.linalg.norm(vetor_professor - vetor_recurso)
        
        # Distância máxima possível (diagonal do hipercubo unitário)
        dimensoes = len(vetor_professor)
        distancia_maxima = np.sqrt(dimensoes)
        
        # Converte distância em similaridade (inverte e normaliza)
        similaridade = max(0, 1 - (distancia / distancia_maxima))
        
        return similaridade
    
    def _construir_vetor_professor(self):
        """
        Constrói vetor de características do perfil do professor
        
        Returns:
            numpy.array: Vetor 5D normalizado [0-1]
        """
        return np.array([
            self.respostas.familiaridadeTech,      # Dimensão 1: Habilidade tech
            self.respostas.tempoPreparacao,         # Dimensão 2: Tempo disponível
            self.respostas.conectividade,           # Dimensão 3: Infraestrutura
            self.respostas.engajamento,             # Dimensão 4: Engajamento turma
            self.respostas.desempenho               # Dimensão 5: Desempenho turma
        ])
    
    def _construir_vetor_recurso(self, recurso):
        """
        Constrói vetor de características do recurso
        
        Returns:
            numpy.array: Vetor 5D normalizado [0-1]
        """
        return np.array([
            recurso.facilidadeUso,                  # Dimensão 1: Facilidade
            recurso.adaptabilidadePedagogica,       # Dimensão 2: Flexibilidade
            recurso.requisitosInfraestrutura,       # Dimensão 3: Requisitos
            recurso.engajamentoPotencial,           # Dimensão 4: Engajamento
            recurso.custoAcessibilidade             # Dimensão 5: Acessibilidade
        ])
    
    def calcular_centroide_cluster(self, recursos):
        """
        Calcula centróide do cluster de recursos elegíveis
        Útil para visualização e análise
        
        Returns:
            numpy.array: Vetor centróide médio
        """
        if not recursos:
            return np.zeros(5)
        
        vetores = [self._construir_vetor_recurso(r) for r in recursos]
        return np.mean(vetores, axis=0)
    
    def obter_distancias_detalhadas(self, recurso):
        """
        Retorna distâncias por dimensão para explicabilidade
        
        Returns:
            dict: Distâncias em cada dimensão
        """
        vetor_prof = self._construir_vetor_professor()
        vetor_rec = self._construir_vetor_recurso(recurso)
        
        return {
            'familiaridade_facilidade': abs(vetor_prof[0] - vetor_rec[0]),
            'tempo_adaptabilidade': abs(vetor_prof[1] - vetor_rec[1]),
            'infraestrutura': abs(vetor_prof[2] - vetor_rec[2]),
            'engajamento': abs(vetor_prof[3] - vetor_rec[3]),
            'desempenho_acessibilidade': abs(vetor_prof[4] - vetor_rec[4])
        }