"""
FUNÇÃO 3: AGRUPAMENTO (K-Means Clustering + Similaridade)
Calcula distância euclidiana E identifica clusters naturais
Baseado em: Scikit-learn KMeans
Referências:
- MacQueen, J. (1967). Some methods for classification and analysis
- Arthur, D., & Vassilvitskii, S. (2007). k-means++: The advantages
- Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python
"""
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

class AgrupadorSimilaridade:
    """
    Implementa clustering e cálculo de similaridade
    """
    
    def __init__(self, respostas):
        self.respostas = respostas
        self.scaler = StandardScaler()
        self.modelo_kmeans = None
        self.labels_recursos = None
        self.centroides = None
        self.metricas_clustering = {}
        
    def calcular_similaridade(self, recurso):
        """
        Calcula similaridade usando distância euclidiana normalizada
        (Método original mantido)
        """
        vetor_professor = self._construir_vetor_professor()
        vetor_recurso = self._construir_vetor_recurso(recurso)
        
        distancia = np.linalg.norm(vetor_professor - vetor_recurso)
        dimensoes = len(vetor_professor)
        distancia_maxima = np.sqrt(dimensoes)
        
        similaridade = max(0, 1 - (distancia / distancia_maxima))
        
        return similaridade
    
    def agrupar_recursos(self, recursos, n_clusters=5, metodo='kmeans'):
        """
        Agrupa recursos em clusters usando K-Means ou DBSCAN
        
        Args:
            recursos: Lista de recursos
            n_clusters: Número de clusters (apenas para K-Means)
            metodo: 'kmeans' ou 'dbscan'
        
        Returns:
            dict: Informações sobre clusters
        """
        # Construir matriz de features dos recursos
        X = np.array([self._construir_vetor_recurso(r) for r in recursos])
        
        # Normalizar features
        X_scaled = self.scaler.fit_transform(X)
        
        if metodo == 'kmeans':
            return self._kmeans_clustering(X_scaled, recursos, n_clusters)
        elif metodo == 'dbscan':
            return self._dbscan_clustering(X_scaled, recursos)
        else:
            raise ValueError(f"Método '{metodo}' não suportado")
    
    def _kmeans_clustering(self, X_scaled, recursos, n_clusters):
        """
        Aplica K-Means clustering
        """
        # Determinar melhor número de clusters se não especificado
        if n_clusters == 'auto':
            n_clusters = self._determinar_n_clusters_otimo(X_scaled)
        
        # Aplicar K-Means
        self.modelo_kmeans = KMeans(
            n_clusters=n_clusters,
            init='k-means++',      # Inicialização inteligente
            n_init=10,             # Número de execuções
            max_iter=300,
            random_state=42
        )
        
        # Treinar e prever
        self.labels_recursos = self.modelo_kmeans.fit_predict(X_scaled)
        self.centroides = self.modelo_kmeans.cluster_centers_
        
        # Calcular métricas de qualidade
        if n_clusters > 1 and len(np.unique(self.labels_recursos)) > 1:
            silhouette = silhouette_score(X_scaled, self.labels_recursos)
            davies_bouldin = davies_bouldin_score(X_scaled, self.labels_recursos)
            calinski = calinski_harabasz_score(X_scaled, self.labels_recursos)
        else:
            silhouette = davies_bouldin = calinski = 0.0
        
        self.metricas_clustering = {
            'n_clusters': n_clusters,
            'inertia': self.modelo_kmeans.inertia_,
            'silhouette_score': silhouette,
            'davies_bouldin_index': davies_bouldin,
            'calinski_harabasz_score': calinski,
            'metodo': 'K-Means'
        }
        
        # Organizar recursos por cluster
        clusters = {}
        for i, label in enumerate(self.labels_recursos):
            if label not in clusters:
                clusters[label] = {
                    'recursos': [],
                    'centroide': self.centroides[label].tolist(),
                    'tamanho': 0
                }
            clusters[label]['recursos'].append({
                'id': recursos[i].id,
                'nome': recursos[i].nome,
                'area': recursos[i].area,
                'distancia_centroide': float(
                    np.linalg.norm(X_scaled[i] - self.centroides[label])
                )
            })
            clusters[label]['tamanho'] += 1
        
        # Identificar características de cada cluster
        for label, cluster in clusters.items():
            cluster['caracteristicas'] = self._identificar_caracteristicas_cluster(
                cluster['recursos'], recursos
            )
        
        return {
            'clusters': clusters,
            'metricas': self.metricas_clustering,
            'labels': self.labels_recursos.tolist()
        }
    
    def _dbscan_clustering(self, X_scaled, recursos):
        """
        Aplica DBSCAN clustering (densidade)
        """
        # DBSCAN não requer número de clusters predefinido
        modelo_dbscan = DBSCAN(
            eps=0.5,           # Raio de vizinhança
            min_samples=3,     # Mínimo de pontos para formar cluster
            metric='euclidean'
        )
        
        labels = modelo_dbscan.fit_predict(X_scaled)
        
        # Organizar resultados
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = list(labels).count(-1)
        
        clusters = {}
        for i, label in enumerate(labels):
            if label == -1:  # Ruído
                continue
            
            if label not in clusters:
                clusters[label] = {
                    'recursos': [],
                    'tamanho': 0
                }
            
            clusters[label]['recursos'].append({
                'id': recursos[i].id,
                'nome': recursos[i].nome,
                'area': recursos[i].area
            })
            clusters[label]['tamanho'] += 1
        
        return {
            'clusters': clusters,
            'metricas': {
                'n_clusters': n_clusters,
                'n_noise': n_noise,
                'metodo': 'DBSCAN'
            },
            'labels': labels.tolist()
        }
    
    def _determinar_n_clusters_otimo(self, X_scaled, max_k=8):
        """
        Determina número ótimo de clusters usando Método do Cotovelo + Silhouette
        
        Returns:
            int: Número ótimo de clusters
        """
        inertias = []
        silhouettes = []
        K_range = range(2, min(max_k + 1, len(X_scaled)))
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42, n_init=10)
            labels = kmeans.fit_predict(X_scaled)
            
            inertias.append(kmeans.inertia_)
            
            if len(np.unique(labels)) > 1:
                silhouettes.append(silhouette_score(X_scaled, labels))
            else:
                silhouettes.append(0)
        
        # Escolher k com melhor silhouette
        k_otimo = K_range[np.argmax(silhouettes)]
        
        return k_otimo
    
    def identificar_cluster_professor(self, clusters_recursos):
        """
        Identifica a qual cluster de recursos o professor está mais próximo
        
        Returns:
            dict: Cluster mais próximo e distância
        """
        vetor_professor = self._construir_vetor_professor()
        
        distancias_centroides = {}
        
        for label, cluster in clusters_recursos['clusters'].items():
            centroide = np.array(cluster['centroide'])
            distancia = np.linalg.norm(vetor_professor - centroide)
            distancias_centroides[label] = float(distancia)
        
        cluster_mais_proximo = min(distancias_centroides, key=distancias_centroides.get)
        
        return {
            'cluster_id': int(cluster_mais_proximo),
            'distancia': distancias_centroides[cluster_mais_proximo],
            'recursos_cluster': clusters_recursos['clusters'][cluster_mais_proximo]['recursos'],
            'caracteristicas': clusters_recursos['clusters'][cluster_mais_proximo].get('caracteristicas', {})
        }
    
    def _identificar_caracteristicas_cluster(self, recursos_cluster, todos_recursos):
        """
        Identifica características dominantes de um cluster
        
        Returns:
            dict: Características do cluster
        """
        # Mapear IDs para recursos
        recursos_obj = []
        for rc in recursos_cluster:
            for r in todos_recursos:
                if r.id == rc['id']:
                    recursos_obj.append(r)
                    break
        
        if not recursos_obj:
            return {}
        
        # Calcular médias
        facilidade_media = np.mean([r.facilidadeUso for r in recursos_obj])
        engajamento_medio = np.mean([r.engajamentoPotencial for r in recursos_obj])
        adaptabilidade_media = np.mean([r.adaptabilidadePedagogica for r in recursos_obj])
        acessibilidade_media = np.mean([r.custoAcessibilidade for r in recursos_obj])
        
        # Identificar tags predominantes
        todas_tags = []
        for r in recursos_obj:
            todas_tags.extend(r.tags)
        
        from collections import Counter
        tags_comuns = Counter(todas_tags).most_common(3)
        
        # Identificar áreas
        areas = [r.area for r in recursos_obj]
        area_predominante = Counter(areas).most_common(1)[0][0]
        
        # Identificar se tem avaliação
        com_avaliacao = sum(1 for r in recursos_obj if r.avaliacao)
        taxa_avaliacao = com_avaliacao / len(recursos_obj)
        
        # Identificar offline
        offline = sum(1 for r in recursos_obj if r.offline)
        taxa_offline = offline / len(recursos_obj)
        
        # Classificar perfil do cluster
        perfil = self._classificar_perfil_cluster(
            facilidade_media,
            engajamento_medio,
            adaptabilidade_media,
            tags_comuns
        )
        
        return {
            'facilidade_media': round(facilidade_media, 2),
            'engajamento_medio': round(engajamento_medio, 2),
            'adaptabilidade_media': round(adaptabilidade_media, 2),
            'acessibilidade_media': round(acessibilidade_media, 2),
            'tags_predominantes': [tag for tag, _ in tags_comuns],
            'area_predominante': area_predominante,
            'taxa_com_avaliacao': round(taxa_avaliacao, 2),
            'taxa_offline': round(taxa_offline, 2),
            'perfil': perfil
        }
    
    def _classificar_perfil_cluster(self, facilidade, engajamento, adaptabilidade, tags_comuns):
        """
        Classifica o perfil do cluster baseado nas características
        
        Returns:
            str: Nome do perfil
        """
        tags = [tag for tag, _ in tags_comuns]
        
        # Cluster Iniciante-Friendly
        if facilidade >= 0.85 and engajamento >= 0.80:
            return "Iniciante-Friendly (fácil e engajador)"
        
        # Cluster Avançado-Investigativo
        elif adaptabilidade >= 0.85 and 'investigativo' in tags:
            return "Avançado-Investigativo (complexo e exploratório)"
        
        # Cluster Gamificação
        elif engajamento >= 0.90 and 'revisao' in tags:
            return "Gamificação e Revisão (motivador para provas)"
        
        # Cluster Colaborativo
        elif adaptabilidade >= 0.90 and 'projetos' in tags:
            return "Colaborativo-Criativo (trabalho em grupo)"
        
        # Cluster Laboratório Virtual
        elif 'pratica' in tags and engajamento >= 0.85:
            return "Laboratório Virtual (experimentação prática)"
        
        # Cluster Genérico
        else:
            return "Multifuncional (uso geral)"
    
    def visualizar_clusters_2d(self, X_scaled):
        """
        Reduz dimensionalidade para 2D usando PCA e retorna coordenadas
        
        Returns:
            dict: Coordenadas 2D dos recursos e centroides
        """
        if self.modelo_kmeans is None:
            return None
        
        # Aplicar PCA para reduzir para 2D
        pca = PCA(n_components=2, random_state=42)
        X_2d = pca.fit_transform(X_scaled)
        centroides_2d = pca.transform(self.centroides)
        
        return {
            'recursos_2d': X_2d.tolist(),
            'centroides_2d': centroides_2d.tolist(),
            'variancia_explicada': pca.explained_variance_ratio_.tolist()
        }
    
    def calcular_centroide_cluster(self, recursos):
        """
        Calcula centróide do cluster de recursos elegíveis
        (Método original mantido)
        """
        if not recursos:
            return np.zeros(5)
        
        vetores = [self._construir_vetor_recurso(r) for r in recursos]
        return np.mean(vetores, axis=0)
    
    def obter_distancias_detalhadas(self, recurso):
        """
        Retorna distâncias por dimensão
        (Método original mantido)
        """
        vetor_prof = self._construir_vetor_professor()
        vetor_rec = self._construir_vetor_recurso(recurso)
        
        return {
            'familiaridade_facilidade': float(abs(vetor_prof[0] - vetor_rec[0])),
            'tempo_adaptabilidade': float(abs(vetor_prof[1] - vetor_rec[1])),
            'infraestrutura': float(abs(vetor_prof[2] - vetor_rec[2])),
            'engajamento': float(abs(vetor_prof[3] - vetor_rec[3])),
            'desempenho_acessibilidade': float(abs(vetor_prof[4] - vetor_rec[4]))
        }
    
    def _construir_vetor_professor(self):
        """Constrói vetor 5D do professor"""
        return np.array([
            self.respostas.familiaridadeTech,
            self.respostas.tempoPreparacao,
            self.respostas.conectividade,
            self.respostas.engajamento,
            self.respostas.desempenho
        ])
    
    def _construir_vetor_recurso(self, recurso):
        """Constrói vetor 5D do recurso"""
        return np.array([
            recurso.facilidadeUso,
            recurso.adaptabilidadePedagogica,
            recurso.requisitosInfraestrutura,
            recurso.engajamentoPotencial,
            recurso.custoAcessibilidade
        ])