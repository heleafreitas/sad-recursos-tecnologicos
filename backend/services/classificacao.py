"""
FUNÇÃO 1: CLASSIFICAÇÃO (Decision Tree Logic)
Implementa regras de decisão para filtrar recursos incompatíveis
Baseado em: Scikit-learn Decision Trees e regras de negócio
"""
from config import Config

class ClassificadorRecursos:
    """
    Aplica árvore de decisão para classificar recursos como elegíveis ou não
    """
    
    def __init__(self, respostas):
        self.respostas = respostas
    
    def filtrar_recursos_elegiveis(self, recursos):
        """
        Aplica 6 regras de classificação para filtrar recursos
        
        Returns:
            list: Recursos que passaram em todas as regras
        """
        elegiveis = []
        
        for recurso in recursos:
            if self._aplicar_regras_decisao(recurso):
                elegiveis.append(recurso)
        
        return elegiveis
    
    def _aplicar_regras_decisao(self, recurso):
        """
        Árvore de decisão com 6 regras principais
        
        Returns:
            bool: True se recurso passa em todas as regras
        """
        # REGRA 1: Compatibilidade de disciplina
        if not self._regra_compatibilidade_disciplina(recurso):
            return False
        
        # REGRA 2: Familiaridade tecnológica vs Facilidade de uso
        if not self._regra_familiaridade_tecnologica(recurso):
            return False
        
        # REGRA 3: Compatibilidade com dispositivos
        if not self._regra_dispositivos(recurso):
            return False
        
        # REGRA 4: Conectividade
        if not self._regra_conectividade(recurso):
            return False
        
        # REGRA 5: Modalidade de ensino
        if not self._regra_modalidade(recurso):
            return False
        
        # REGRA 6: Necessidade de avaliação
        if not self._regra_avaliacao(recurso):
            return False
        
        return True
    
    def _regra_compatibilidade_disciplina(self, recurso):
        """Verifica se recurso é compatível com a disciplina"""
        if recurso.area == 'Multidisciplinar':
            return True
        
        if recurso.area == self.respostas.disciplina:
            return True
        
        # Caso especial: Ciências
        disciplinas_ciencias = ['Física', 'Química', 'Biologia']
        if (self.respostas.disciplina in disciplinas_ciencias and 
            'Física/Química/Biologia' in recurso.area):
            return True
        
        return False
    
    def _regra_familiaridade_tecnologica(self, recurso):
        """
        Professores com baixa familiaridade precisam de ferramentas fáceis
        """
        if (self.respostas.familiaridadeTech < Config.LIMIAR_FAMILIARIDADE_BAIXA and 
            recurso.facilidadeUso < Config.LIMIAR_FACILIDADE_MINIMA):
            return False
        return True
    
    def _regra_dispositivos(self, recurso):
        """Verifica disponibilidade de dispositivos"""
        if 'nenhum' in self.respostas.acessoDispositivos:
            # Alunos não têm dispositivos, precisa de lab
            if 'laboratorio' not in self.respostas.infraestrutura:
                return False
            # Lab disponível, recurso precisa funcionar em computador
            if 'computador' not in recurso.dispositivos:
                return False
        
        return True
    
    def _regra_conectividade(self, recurso):
        """Verifica se conectividade é suficiente"""
        if (self.respostas.conectividade < Config.LIMIAR_CONECTIVIDADE_OFFLINE and 
            not recurso.offline):
            return False
        return True
    
    def _regra_modalidade(self, recurso):
        """Verifica compatibilidade com modalidade de aula"""
        return self.respostas.modalidade in recurso.modalidades
    
    def _regra_avaliacao(self, recurso):
        """Verifica necessidade de avaliação automática"""
        if self.respostas.necessidadeAvaliacao and not recurso.avaliacao:
            return False
        return True