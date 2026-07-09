# Sistema de Apoio à Decisão - Recursos Tecnológicos Educacionais

Sistema completo de recomendação de recursos tecnológicos para professores do 3º ano do ensino médio, utilizando técnicas avançadas de análise de dados.

## 🏗️ Arquitetura

- **Frontend**: React 18 + Vite + TailwindCSS
- **Backend**: Python 3.11 + Flask + Scikit-learn
- **Análise de Dados**: NumPy, Pandas, Scikit-learn

## 🧮 Funções de Análise Implementadas

### 1. **Classificação (Decision Tree Logic)**
- Filtra recursos incompatíveis usando árvore de decisão
- 6 regras de negócio baseadas em requisitos técnicos e pedagógicos
- Biblioteca: Lógica customizada inspirada em Scikit-learn

### 2. **Análise de Associação (Association Rules)**
- Identifica padrões entre contexto do professor e recursos adequados
- 5 regras de associação (estilo ensino, objetivos, engajamento, etc.)
- Biblioteca: NumPy para cálculos vetorizados
- Peso: 35% do score final

### 3. **Agrupamento por Similaridade (K-Means Adaptado)**
- Calcula distância euclidiana entre perfil do professor e recursos
- Vetores 5D normalizados para comparação
- Biblioteca: NumPy + Scikit-learn (MinMaxScaler)
- Peso: 35% do score final

## 🚀 Como Executar

### Backend (Python)
```bash
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate

# Ativar ambiente (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python app.py
```

Servidor rodará em: `http://localhost:5000`

### Frontend (React)
```bash
cd frontend

# Instalar dependências
npm install

# Executar em modo desenvolvimento
npm run dev
```

Aplicação rodará em: `http://localhost:3000`

## 📊 API Endpoints

### `GET /api/recursos`
Lista todos os recursos tecnológicos disponíveis

### `POST /api/recomendacoes`
Gera ranking de recomendações baseado nas respostas do questionário

**Body:**
```json
{
  "disciplina": "Matemática",
  "familiaridadeTech": 0.6,
  "estiloEnsino": "investigativo",
  "objetivoAula": "pratica",
  ...
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "ranking": [...],
    "analises": {
      "totalRecursos": 10,
      "recursosElegiveis": 7,
      "taxaFiltragem": 30.0,
      "principalCriterio": "Associação"
    }
  }
}
```

### `GET /api/metodologia`
Retorna informações sobre a metodologia de análise
