"""
FUNÇÃO 1: CLASSIFICAÇÃO COM DECISION TREE (Scikit-learn)
Implementa árvore de decisão para classificar recursos como elegíveis ou não elegíveis
"""
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

class ClassificadorRecursos:
    """Decision Tree Classifier para filtrar recursos elegíveis"""
    
    def __init__(self, respostas):
        self.respostas = respostas
        self.modelo = None
        self.feature_names = []
        self.historico_treinamento = []
        
    def construir_features_recurso(self, recurso):
        """Constrói vetor de features para um recurso"""
        compat_disciplina = 1.0 if self._check_compatibilidade_disciplina(recurso) else 0.0
        adequacao_familiaridade = 1.0
        if self.respostas.familiaridadeTech < 0.5 and recurso.facilidadeUso < 0.7:
            adequacao_familiaridade = 0.0
        elif self.respostas.familiaridadeTech < 0.5:
            adequacao_familiaridade = recurso.facilidadeUso
        
        compat_dispositivos = self._check_dispositivos(recurso)
        adequacao_conectividade = 1.0
        if self.respostas.conectividade < 0.4 and not recurso.offline:
            adequacao_conectividade = 0.0
        
        compat_modalidade = 1.0 if self.respostas.modalidade in recurso.modalidades else 0.0
        
        atende_avaliacao = 1.0
        if self.respostas.necessidadeAvaliacao and not recurso.avaliacao:
            atende_avaliacao = 0.0
        
        facilidade = recurso.facilidadeUso
        engajamento = recurso.engajamentoPotencial
        adaptabilidade = recurso.adaptabilidadePedagogica
        requisitos_infra = recurso.requisitosInfraestrutura
        acessibilidade = recurso.custoAcessibilidade
        match_estilo = 1.0 if self.respostas.estiloEnsino in recurso.tags else 0.0
        match_objetivo = 1.0 if self.respostas.objetivoAula in recurso.tags else 0.0
        funciona_offline = 1.0 if recurso.offline else 0.0
        ratio_fam_fac = min(1.0, self.respostas.familiaridadeTech / max(0.1, recurso.facilidadeUso))
        
        return np.array([
            compat_disciplina, adequacao_familiaridade, compat_dispositivos,
            adequacao_conectividade, compat_modalidade, atende_avaliacao,
            facilidade, engajamento, adaptabilidade, requisitos_infra,
            acessibilidade, match_estilo, match_objetivo, funciona_offline,
            ratio_fam_fac
        ])
    
    def gerar_dados_treinamento(self, recursos):
        """Gera dataset de treinamento"""
        X = []
        y = []
        
        for recurso in recursos:
            features = self.construir_features_recurso(recurso)
            X.append(features)
            elegivel = self._aplicar_regras_negocio(recurso)
            y.append(1 if elegivel else 0)
        
        self.feature_names = [
            'Compatibilidade Disciplina', 'Adequação Familiaridade',
            'Compatibilidade Dispositivos', 'Adequação Conectividade',
            'Compatibilidade Modalidade', 'Atende Avaliação', 'Facilidade de Uso',
            'Engajamento Potencial', 'Adaptabilidade Pedagógica',
            'Requisitos Infraestrutura', 'Custo/Acessibilidade',
            'Match Estilo Ensino', 'Match Objetivo Aula', 'Funciona Offline',
            'Ratio Familiaridade/Facilidade'
        ]
        
        return np.array(X), np.array(y)
    
    def treinar_modelo(self, X, y):
        """Treina Decision Tree Classifier"""
        self.modelo = DecisionTreeClassifier(
            criterion='gini', max_depth=5, min_samples_split=3,
            min_samples_leaf=2, random_state=42, class_weight='balanced'
        )
        
        self.modelo.fit(X, y)
        y_pred = self.modelo.predict(X)
        accuracy = accuracy_score(y, y_pred)
        cv_scores = cross_val_score(self.modelo, X, y, cv=min(5, len(X)), scoring='accuracy')
        
        self.historico_treinamento.append({
            'accuracy_treino': accuracy,
            'cv_accuracy_mean': cv_scores.mean(),
            'cv_accuracy_std': cv_scores.std(),
            'n_samples': len(X),
            'n_elegivel': np.sum(y == 1),
            'n_inelegivel': np.sum(y == 0)
        })
        
        return self.modelo
    
    def filtrar_recursos_elegiveis(self, recursos):
        """Filtra recursos elegíveis usando Decision Tree"""
        X, y = self.gerar_dados_treinamento(recursos)
        self.treinar_modelo(X, y)
        predicoes = self.modelo.predict(X)
        recursos_elegiveis = [recurso for i, recurso in enumerate(recursos) if predicoes[i] == 1]
        return recursos_elegiveis
    
    def obter_importancia_features(self):
        """Retorna importância de cada feature"""
        if self.modelo is None:
            return {}
        importancias = self.modelo.feature_importances_
        return {nome: float(imp) for nome, imp in zip(self.feature_names, importancias)}
    
    def _aplicar_regras_negocio(self, recurso):
        """Aplica regras de negócio para determinar elegibilidade"""
        if not self._check_compatibilidade_disciplina(recurso):
            return False
        if self.respostas.familiaridadeTech < 0.5 and recurso.facilidadeUso < 0.7:
            return False
        if not self._check_dispositivos(recurso):
            return False
        if self.respostas.conectividade < 0.4 and not recurso.offline:
            return False
        if self.respostas.modalidade not in recurso.modalidades:
            return False
        if self.respostas.necessidadeAvaliacao and not recurso.avaliacao:
            return False
        return True
    
    def _check_compatibilidade_disciplina(self, recurso):
        """Verifica compatibilidade de disciplina"""
        if recurso.area == 'Multidisciplinar':
            return True
        if recurso.area == self.respostas.disciplina:
            return True
        return False
    
    def _check_dispositivos(self, recurso):
        """Verifica disponibilidade de dispositivos"""
        return True
