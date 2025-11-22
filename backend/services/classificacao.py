"""
FUNÇÃO 1: CLASSIFICAÇÃO COM DECISION TREE (Scikit-learn)
Implementa árvore de decisão para classificar recursos como elegíveis ou não elegíveis
Baseado em: Scikit-learn DecisionTreeClassifier
Referências:
- Breiman, L., et al. (1984). Classification and Regression Trees (CART)
- Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python
- Quinlan, J. R. (1986). Induction of decision trees
"""
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib
matplotlib.use('Agg')  # Backend não-interativo
import matplotlib.pyplot as plt
import io
import base64

class ClassificadorRecursos:
    """
    Implementa Decision Tree Classifier para filtrar recursos elegíveis
    """
    
    def __init__(self, respostas):
        self.respostas = respostas
        self.modelo = None
        self.label_encoder = LabelEncoder()
        self.feature_names = []
        self.historico_treinamento = []
        
    def construir_features_recurso(self, recurso):
        """
        Constrói vetor de features para um recurso
        
        Returns:
            numpy.array: Vetor de 15 features binárias/contínuas
        """
        # FEATURE 1: Compatibilidade de disciplina (0 ou 1)
        compat_disciplina = 1.0 if self._check_compatibilidade_disciplina(recurso) else 0.0
        
        # FEATURE 2: Adequação à familiaridade tecnológica (0-1)
        adequacao_familiaridade = 1.0
        if self.respostas.familiaridadeTech < 0.5 and recurso.facilidadeUso < 0.7:
            adequacao_familiaridade = 0.0
        elif self.respostas.familiaridadeTech < 0.5:
            adequacao_familiaridade = recurso.facilidadeUso
        
        # FEATURE 3: Disponibilidade de dispositivos (0 ou 1)
        compat_dispositivos = self._check_dispositivos(recurso)
        
        # FEATURE 4: Adequação à conectividade (0 ou 1)
        adequacao_conectividade = 1.0
        if self.respostas.conectividade < 0.4 and not recurso.offline:
            adequacao_conectividade = 0.0
        
        # FEATURE 5: Compatibilidade com modalidade (0 ou 1)
        compat_modalidade = 1.0 if self.respostas.modalidade in recurso.modalidades else 0.0
        
        # FEATURE 6: Atende necessidade de avaliação (0 ou 1)
        atende_avaliacao = 1.0
        if self.respostas.necessidadeAvaliacao and not recurso.avaliacao:
            atende_avaliacao = 0.0
        
        # FEATURE 7: Facilidade de uso do recurso (0-1)
        facilidade = recurso.facilidadeUso
        
        # FEATURE 8: Engajamento potencial (0-1)
        engajamento = recurso.engajamentoPotencial
        
        # FEATURE 9: Adaptabilidade pedagógica (0-1)
        adaptabilidade = recurso.adaptabilidadePedagogica
        
        # FEATURE 10: Requisitos de infraestrutura (0-1)
        requisitos_infra = recurso.requisitosInfraestrutura
        
        # FEATURE 11: Custo e acessibilidade (0-1)
        acessibilidade = recurso.custoAcessibilidade
        
        # FEATURE 12: Match estilo de ensino (0 ou 1)
        match_estilo = 1.0 if self.respostas.estiloEnsino in recurso.tags else 0.0
        
        # FEATURE 13: Match objetivo da aula (0 ou 1)
        match_objetivo = 1.0 if self.respostas.objetivoAula in recurso.tags else 0.0
        
        # FEATURE 14: Funciona offline (0 ou 1)
        funciona_offline = 1.0 if recurso.offline else 0.0
        
        # FEATURE 15: Ratio familiaridade/facilidade
        ratio_fam_fac = min(1.0, self.respostas.familiaridadeTech / max(0.1, recurso.facilidadeUso))
        
        return np.array([
            compat_disciplina,
            adequacao_familiaridade,
            compat_dispositivos,
            adequacao_conectividade,
            compat_modalidade,
            atende_avaliacao,
            facilidade,
            engajamento,
            adaptabilidade,
            requisitos_infra,
            acessibilidade,
            match_estilo,
            match_objetivo,
            funciona_offline,
            ratio_fam_fac
        ])
    
    def gerar_dados_treinamento(self, recursos):
        """
        Gera dataset de treinamento aplicando regras de negócio
        
        Returns:
            X: numpy.array - Matriz de features (n_recursos, 15)
            y: numpy.array - Vetor de labels (n_recursos,) [0=inelegível, 1=elegível]
        """
        X = []
        y = []
        
        for recurso in recursos:
            # Construir features
            features = self.construir_features_recurso(recurso)
            X.append(features)
            
            # Label baseado em regras de negócio (ground truth)
            elegivel = self._aplicar_regras_negocio(recurso)
            y.append(1 if elegivel else 0)
        
        self.feature_names = [
            'Compatibilidade Disciplina',
            'Adequação Familiaridade',
            'Compatibilidade Dispositivos',
            'Adequação Conectividade',
            'Compatibilidade Modalidade',
            'Atende Avaliação',
            'Facilidade de Uso',
            'Engajamento Potencial',
            'Adaptabilidade Pedagógica',
            'Requisitos Infraestrutura',
            'Custo/Acessibilidade',
            'Match Estilo Ensino',
            'Match Objetivo Aula',
            'Funciona Offline',
            'Ratio Familiaridade/Facilidade'
        ]
        
        return np.array(X), np.array(y)
    
    def treinar_modelo(self, X, y):
        """
        Treina Decision Tree Classifier
        
        Args:
            X: Matriz de features
            y: Vetor de labels
        
        Returns:
            modelo treinado
        """
        # Criar modelo de Decision Tree
        self.modelo = DecisionTreeClassifier(
            criterion='gini',           # Critério de divisão: Gini impurity
            max_depth=5,                # Profundidade máxima (evita overfitting)
            min_samples_split=3,        # Mínimo de amostras para split
            min_samples_leaf=2,         # Mínimo de amostras nas folhas
            random_state=42,            # Reprodutibilidade
            class_weight='balanced'     # Balanceia classes desbalanceadas
        )
        
        # Treinar
        self.modelo.fit(X, y)
        
        # Calcular métricas
        y_pred = self.modelo.predict(X)
        accuracy = accuracy_score(y, y_pred)
        
        # Cross-validation (5-fold)
        cv_scores = cross_val_score(self.modelo, X, y, cv=min(5, len(X)), scoring='accuracy')
        
        # Importância das features
        importancias = self.modelo.feature_importances_
        
        # Armazenar histórico
        self.historico_treinamento.append({
            'accuracy_treino': accuracy,
            'cv_accuracy_mean': cv_scores.mean(),
            'cv_accuracy_std': cv_scores.std(),
            'feature_importances': importancias.tolist(),
            'n_samples': len(X),
            'n_elegivel': np.sum(y == 1),
            'n_inelegivel': np.sum(y == 0)
        })
        
        return self.modelo
    
    def filtrar_recursos_elegiveis(self, recursos):
        """
        Filtra recursos elegíveis usando Decision Tree treinada
        
        Returns:
            list: Recursos classificados como elegíveis
        """
        # Gerar dados de treinamento
        X, y = self.gerar_dados_treinamento(recursos)
        
        # Treinar modelo
        self.treinar_modelo(X, y)
        
        # Predizer elegibilidade
        predicoes = self.modelo.predict(X)
        
        # Filtrar recursos elegíveis (predição = 1)
        recursos_elegiveis = [
            recurso for i, recurso in enumerate(recursos)
            if predicoes[i] == 1
        ]
        
        return recursos_elegiveis
    
    def obter_importancia_features(self):
        """
        Retorna importância de cada feature na decisão
        
        Returns:
            dict: Feature name -> Importância
        """
        if self.modelo is None:
            return {}
        
        importancias = self.modelo.feature_importances_
        
        importancia_dict = {
            nome: float(imp)
            for nome, imp in zip(self.feature_names, importancias)
        }
        
        # Ordenar por importância
        importancia_ordenada = dict(
            sorted(importancia_dict.items(), key=lambda x: x[1], reverse=True)
        )
        
        return importancia_ordenada
    
    def exportar_regras_texto(self):
        """
        Exporta árvore de decisão em formato texto legível
        
        Returns:
            str: Representação textual da árvore
        """
        if self.modelo is None:
            return "Modelo não treinado"
        
        tree_rules = export_text(
            self.modelo,
            feature_names=self.feature_names,
            max_depth=5,
            decimals=2
        )
        
        return tree_rules
    
    def visualizar_arvore(self):
        """
        Gera visualização da árvore de decisão em base64
        
        Returns:
            str: Imagem em base64
        """
        if self.modelo is None:
            return None
        
        try:
            plt.figure(figsize=(20, 10))
            plot_tree(
                self.modelo,
                feature_names=self.feature_names,
                class_names=['Inelegível', 'Elegível'],
                filled=True,
                rounded=True,
                fontsize=8,
                max_depth=3  # Limita profundidade para legibilidade
            )
            
            # Salvar em buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            
            # Converter para base64
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            plt.close()
            return img_base64
            
        except Exception as e:
            print(f"Erro ao gerar visualização: {e}")
            return None
    
    def obter_diagnostico(self):
        """
        Retorna diagnóstico completo do modelo
        
        Returns:
            dict: Métricas e informações da árvore
        """
        if not self.historico_treinamento:
            return {'erro': 'Modelo não treinado'}
        
        ultimo_treino = self.historico_treinamento[-1]
        
        diagnostico = {
            'metricas': {
                'accuracy_treino': ultimo_treino['accuracy_treino'],
                'cv_accuracy_mean': ultimo_treino['cv_accuracy_mean'],
                'cv_accuracy_std': ultimo_treino['cv_accuracy_std'],
                'n_samples': ultimo_treino['n_samples'],
                'n_elegivel': ultimo_treino['n_elegivel'],
                'n_inelegivel': ultimo_treino['n_inelegivel'],
                'taxa_elegibilidade': ultimo_treino['n_elegivel'] / ultimo_treino['n_samples']
            },
            'estrutura_arvore': {
                'profundidade_maxima': self.modelo.get_depth(),
                'n_folhas': self.modelo.get_n_leaves(),
                'n_nodes': self.modelo.tree_.node_count
            },
            'importancia_features': self.obter_importancia_features(),
            'regras_texto': self.exportar_regras_texto(),
            'qualidade_modelo': self._avaliar_qualidade(ultimo_treino)
        }
        
        return diagnostico
    
    def _avaliar_qualidade(self, treino):
        """
        Avalia qualidade do modelo
        """
        accuracy = treino['accuracy_treino']
        cv_accuracy = treino['cv_accuracy_mean']
        
        if accuracy >= 0.95 and cv_accuracy >= 0.90:
            return 'Excelente - Modelo muito confiável'
        elif accuracy >= 0.85 and cv_accuracy >= 0.80:
            return 'Bom - Modelo confiável'
        elif accuracy >= 0.75:
            return 'Moderado - Considerar ajustes'
        else:
            return 'Fraco - Necessita revisão das regras'
    
    def _aplicar_regras_negocio(self, recurso):
        """
        Aplica regras de negócio para determinar elegibilidade (ground truth)
        """
        # Regra 1: Compatibilidade de disciplina
        if not self._check_compatibilidade_disciplina(recurso):
            return False
        
        # Regra 2: Familiaridade tecnológica
        if self.respostas.familiaridadeTech < 0.5 and recurso.facilidadeUso < 0.7:
            return False
        
        # Regra 3: Dispositivos
        if not self._check_dispositivos(recurso):
            return False
        
        # Regra 4: Conectividade
        if self.respostas.conectividade < 0.4 and not recurso.offline:
            return False
        
        # Regra 5: Modalidade
        if self.respostas.modalidade not in recurso.modalidades:
            return False
        
        # Regra 6: Avaliação
        if self.respostas.necessidadeAvaliacao and not recurso.avaliacao:
            return False
        
        return True
    
    def _check_compatibilidade_disciplina(self, recurso):
        """Verifica compatibilidade de disciplina"""
        if recurso.area == 'Multidisciplinar':
            return True
        if recurso.area == self.respostas.disciplina:
            return True
        disciplinas_ciencias = ['Física', 'Química', 'Biologia']
        if (self.respostas.disciplina in disciplinas_ciencias and 
            'Física/Química/Biologia' in recurso.area):
            return True
        return False
    
    def _check_dispositivos(self, recurso):
        """Verifica disponibilidade de dispositivos"""
        dispositivosAluno = self.respostas.acessoDispositivos or []
        
        if 'nenhum' in dispositivosAluno and 'computador' not in dispositivosAluno:
            infraEscola = self.respostas.infraestrutura or []
            if 'laboratorio' not in infraEscola:
                return False
            if 'computador' not in recurso.dispositivos:
                return False
        
        return True