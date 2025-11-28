"""
FUNÇÃO 2: AGRUPAMENTO (K-Means Clustering) com Nomes Descritivos
Agrupa recursos e atribui nomes aos clusters baseado em características
"""
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from collections import Counter
import numpy as np

class AgrupadorSimilaridade:
    """Clustering e cálculo de similaridade com nomes descritivos"""
    
    def __init__(self, respostas):
        self.respostas = respostas
        self.scaler = StandardScaler()
        self.modelo_kmeans = None
        self.labels_recursos = None
        self.centroides = None
        self.metricas_clustering = {}
        self.nomes_clusters = {}
        
    def calcular_similaridade(self, recurso):
        """Calcula similaridade usando distância euclidiana normalizada"""
        vetor_professor = self._construir_vetor_professor()
        vetor_recurso = self._construir_vetor_recurso(recurso)
        distancia = np.linalg.norm(vetor_professor - vetor_recurso)
        dimensoes = len(vetor_professor)
        distancia_maxima = np.sqrt(dimensoes)
        similaridade = max(0, 1 - (distancia / distancia_maxima))
        return similaridade
    
    def agrupar_recursos(self, recursos, n_clusters=5):
        """Agrupa recursos em clusters usando K-Means"""
        X = np.array([self._construir_vetor_recurso(r) for r in recursos])
        X_scaled = self.scaler.fit_transform(X)
        
        self.modelo_kmeans = KMeans(
            n_clusters=n_clusters, init='k-means++', n_init=10,
            max_iter=300, random_state=42
        )
        
        self.labels_recursos = self.modelo_kmeans.fit_predict(X_scaled)
        self.centroides = self.modelo_kmeans.cluster_centers_
        
        if n_clusters > 1 and len(np.unique(self.labels_recursos)) > 1:
            silhouette = silhouette_score(X_scaled, self.labels_recursos)
        else:
            silhouette = 0.0
        
        self.metricas_clustering = {
            'n_clusters': n_clusters,
            'inertia': self.modelo_kmeans.inertia_,
            'silhouette_score': silhouette,
            'metodo': 'K-Means'
        }
        
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
                'distancia_centroide': float(np.linalg.norm(X_scaled[i] - self.centroides[label]))
            })
            clusters[label]['tamanho'] += 1
        
        for label, cluster in clusters.items():
            cluster['caracteristicas'] = self._identificar_caracteristicas_cluster(
                cluster['recursos'], recursos
            )
            # Atribui nome ao cluster
            cluster['nome'] = self.nomes_clusters.get(label, f"Cluster {label}")
        
        return {
            'clusters': clusters,
            'metricas': self.metricas_clustering,
            'labels': self.labels_recursos.tolist()
        }
    
    def _identificar_caracteristicas_cluster(self, recursos_cluster, todos_recursos):
        """Identifica características dominantes de um cluster"""
        recursos_obj = []
        for rc in recursos_cluster:
            for r in todos_recursos:
                if r.id == rc['id']:
                    recursos_obj.append(r)
                    break
        
        if not recursos_obj:
            return {}
        
        facilidade_media = np.mean([r.facilidadeUso for r in recursos_obj])
        engajamento_medio = np.mean([r.engajamentoPotencial for r in recursos_obj])
        adaptabilidade_media = np.mean([r.adaptabilidadePedagogica for r in recursos_obj])
        acessibilidade_media = np.mean([r.custoAcessibilidade for r in recursos_obj])
        
        todas_tags = []
        for r in recursos_obj:
            todas_tags.extend(r.tags)
        tags_comuns = Counter(todas_tags).most_common(3)
        
        areas = [r.area for r in recursos_obj]
        area_predominante = Counter(areas).most_common(1)[0][0]
        
        com_avaliacao = sum(1 for r in recursos_obj if r.avaliacao)
        taxa_avaliacao = com_avaliacao / len(recursos_obj)
        
        offline = sum(1 for r in recursos_obj if r.offline)
        taxa_offline = offline / len(recursos_obj)
        
        perfil = self._classificar_perfil_cluster(
            facilidade_media, engajamento_medio, adaptabilidade_media, tags_comuns
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
        """Classifica o perfil do cluster"""
        tags = [tag for tag, _ in tags_comuns]
        
        if facilidade >= 0.85 and engajamento >= 0.80:
            return "Iniciante-Friendly (fácil e engajador)"
        elif adaptabilidade >= 0.85 and 'investigativo' in tags:
            return "Avançado-Investigativo (complexo e exploratório)"
        elif engajamento >= 0.90 and 'revisao' in tags:
            return "Gamificação e Revisão (motivador para provas)"
        elif adaptabilidade >= 0.90 and 'projetos' in tags:
            return "Colaborativo-Criativo (trabalho em grupo)"
        elif 'pratica' in tags and engajamento >= 0.85:
            return "Laboratório Virtual (experimentação prática)"
        else:
            return "Multifuncional (uso geral)"
    
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
    
    def obter_distancias_detalhadas(self, recurso):
        """Retorna distâncias por dimensão"""
        vetor_prof = self._construir_vetor_professor()
        vetor_rec = self._construir_vetor_recurso(recurso)
        
        return {
            'familiaridade_facilidade': float(abs(vetor_prof[0] - vetor_rec[0])),
            'tempo_adaptabilidade': float(abs(vetor_prof[1] - vetor_rec[1])),
            'infraestrutura': float(abs(vetor_prof[2] - vetor_rec[2])),
            'engajamento': float(abs(vetor_prof[3] - vetor_rec[3])),
            'desempenho_acessibilidade': float(abs(vetor_prof[4] - vetor_rec[4]))
        }
