"""
FUNÇÃO 3: REGRESSÃO LINEAR para Definir Pesos do Score Final
Treina modelo de regressão para calcular importância de cada variável
"""
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

class RegressorPesos:
    """Regressão linear para definir pesos das 5 características"""
    
    def __init__(self):
        self.modelo = None
        self.scaler = StandardScaler()
        self.pesos_normalizados = {}
        self.metricas_regressao = {}
    
    def treinar_regressao(self, recursos):
        """
        Treina regressão linear usando as 5 características
        como preditores e adaptabilidade pedagógica como target
        """
        # Construir matriz X (5 características)
        X = np.array([
            [r.facilidadeUso, r.engajamentoPotencial,
             r.adaptabilidadePedagogica, r.requisitosInfraestrutura,
             r.custoAcessibilidade]
            for r in recursos
        ])
        
        # Target: adaptabilidade pedagógica (pode ser ajustado conforme necessidade)
        y = np.array([r.adaptabilidadePedagogica for r in recursos])
        
        # Normalizar features
        X_scaled = self.scaler.fit_transform(X)
        
        # Treinar modelo
        self.modelo = LinearRegression()
        self.modelo.fit(X_scaled, y)
        
        # Calcular métricas
        y_pred = self.modelo.predict(X_scaled)
        r2 = r2_score(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        
        # Extrair coeficientes
        coeficientes = self.modelo.coef_
        
        # Normalizar coeficientes para somar 1.0 (pesos percentuais)
        coef_abs = np.abs(coeficientes)
        pesos_normalizados = coef_abs / np.sum(coef_abs)
        
        # Mapear para nomes das características
        self.pesos_normalizados = {
            'facilidadeUso': float(pesos_normalizados[0]),
            'engajamentoPotencial': float(pesos_normalizados[1]),
            'adaptabilidadePedagogica': float(pesos_normalizados[2]),
            'requisitosInfraestrutura': float(pesos_normalizados[3]),
            'custoAcessibilidade': float(pesos_normalizados[4])
        }
        
        self.metricas_regressao = {
            'r2_score': float(r2),
            'rmse': float(rmse),
            'coeficientes_brutos': coeficientes.tolist(),
            'pesos_normalizados': self.pesos_normalizados,
            'intercepto': float(self.modelo.intercept_)
        }
        
        return self.pesos_normalizados
    
    def obter_pesos(self):
        """Retorna os pesos normalizados"""
        return self.pesos_normalizados
    
    def obter_metricas(self):
        """Retorna métricas da regressão"""
        return self.metricas_regressao

