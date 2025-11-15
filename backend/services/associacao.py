"""
FUNÇÃO 2: ANÁLISE DE ASSOCIAÇÃO (Association Rules)
Identifica padrões entre características do professor/turma e recursos
Baseado em: Apriori Algorithm e Market Basket Analysis
Referência: Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules
"""
import numpy as np

class AnalisadorAssociacao:
    """
    Implementa regras de associação para medir compatibilidade contextual
    """
    
    def __init__(self, respostas):
        self.respostas = respostas
    
    def calcular_score_associacao(self, recurso):
        """
        Calcula score baseado em 5 regras de associação
        
        Formula: Score = Σ(peso_regra * confiança_regra) / total_regras
        
        Returns:
            float: Score de associação [0-1]
        """
        regras = [
            self._regra_estilo_ensino(recurso),
            self._regra_objetivo_aula(recurso),
            self._regra_engajamento_baixo(recurso),
            self._regra_desempenho_baixo(recurso),
            self._regra_tempo_limitado(recurso)
        ]
        
        # Retorna média dos scores das regras
        return np.mean([r for r in regras if r is not None])
    
    def _regra_estilo_ensino(self, recurso):
        """
        Regra: Estilo de ensino → Tags do recurso
        Confidence: 1.0 se match, 0.0 se não
        """
        if self.respostas.estiloEnsino in recurso.tags:
            return 0.25  # 25% do score
        return 0.0
    
    def _regra_objetivo_aula(self, recurso):
        """
        Regra: Objetivo da aula → Tags do recurso
        Confidence: 1.0 se match, 0.0 se não
        """
        if self.respostas.objetivoAula in recurso.tags:
            return 0.25  # 25% do score
        return 0.0
    
    def _regra_engajamento_baixo(self, recurso):
        """
        Regra: Engajamento baixo → Ferramentas com alto potencial de engajamento
        Support: engajamento < 0.5
        Confidence: proporcional ao potencial de engajamento
        """
        if self.respostas.engajamento < 0.5:
            # Quanto maior o potencial de engajamento, maior o score
            if recurso.engajamentoPotencial >= 0.85:
                return 0.20  # 20% do score
            elif recurso.engajamentoPotencial >= 0.70:
                return 0.10  # 10% do score
        return 0.05  # Score mínimo
    
    def _regra_desempenho_baixo(self, recurso):
        """
        Regra: Desempenho baixo → Ferramentas com avaliação automática
        Support: desempenho < 0.5
        Confidence: 1.0 se tem avaliação, 0.5 se não
        """
        if self.respostas.desempenho < 0.5:
            if recurso.avaliacao:
                return 0.15  # 15% do score
            return 0.05
        return 0.10  # Score neutro
    
    def _regra_tempo_limitado(self, recurso):
        """
        Regra: Tempo limitado → Ferramentas fáceis de usar
        Support: tempo < 0.5
        Confidence: proporcional à facilidade de uso
        """
        if self.respostas.tempoPreparacao < 0.5:
            if recurso.facilidadeUso >= 0.85:
                return 0.15  # 15% do score
            elif recurso.facilidadeUso >= 0.70:
                return 0.08
        return 0.05
    
    def obter_regras_ativadas(self, recurso):
        """
        Retorna lista de regras que foram ativadas para explicabilidade
        
        Returns:
            list: Lista de strings descrevendo as regras ativadas
        """
        regras_ativadas = []
        
        if self.respostas.estiloEnsino in recurso.tags:
            regras_ativadas.append(
                f"Compatível com estilo de ensino {self.respostas.estiloEnsino}"
            )
        
        if self.respostas.objetivoAula in recurso.tags:
            regras_ativadas.append(
                f"Adequado para objetivo de {self.respostas.objetivoAula}"
            )
        
        if self.respostas.engajamento < 0.5 and recurso.engajamentoPotencial >= 0.85:
            regras_ativadas.append(
                "Alto potencial para aumentar engajamento da turma"
            )
        
        if self.respostas.desempenho < 0.5 and recurso.avaliacao:
            regras_ativadas.append(
                "Oferece avaliação automática para acompanhar progresso"
            )
        
        if self.respostas.tempoPreparacao < 0.5 and recurso.facilidadeUso >= 0.85:
            regras_ativadas.append(
                "Fácil de preparar e aplicar com tempo limitado"
            )
        
        return regras_ativadas