"""
Modelo para respostas do questionário
"""

class RespostasQuestionario:
    def __init__(self, dados):
        # Perfil do Professor
        self.disciplina = dados.get('disciplina')
        self.familiaridadeTech = float(dados.get('familiaridadeTech', 0.5))
        self.estiloEnsino = dados.get('estiloEnsino')
        self.objetivoAula = dados.get('objetivoAula')
        self.tempoPreparacao = float(dados.get('tempoPreparacao', 0.5))
        
        # Perfil da Turma
        self.tamanhoTurma = int(dados.get('tamanhoTurma', 30))
        self.engajamento = float(dados.get('engajamento', 0.5))
        self.acessoDispositivos = dados.get('acessoDispositivos', [])
        self.conectividade = float(dados.get('conectividade', 0.5))
        self.desempenho = float(dados.get('desempenho', 0.5))
        
        # Contexto Pedagógico
        self.modalidade = dados.get('modalidade')
        self.tempoAula = float(dados.get('tempoAula', 0.5))
        self.necessidadeAvaliacao = dados.get('necessidadeAvaliacao', False)
        self.infraestrutura = dados.get('infraestrutura', [])
    
    def to_dict(self):
        return {
            'disciplina': self.disciplina,
            'familiaridadeTech': self.familiaridadeTech,
            'estiloEnsino': self.estiloEnsino,
            'objetivoAula': self.objetivoAula,
            'tempoPreparacao': self.tempoPreparacao,
            'tamanhoTurma': self.tamanhoTurma,
            'engajamento': self.engajamento,
            'acessoDispositivos': self.acessoDispositivos,
            'conectividade': self.conectividade,
            'desempenho': self.desempenho,
            'modalidade': self.modalidade,
            'tempoAula': self.tempoAula,
            'necessidadeAvaliacao': self.necessidadeAvaliacao,
            'infraestrutura': self.infraestrutura
        }