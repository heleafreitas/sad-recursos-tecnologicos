"""
Modelo de dados para recursos tecnológicos
"""
import json
from pathlib import Path

class RecursoTecnologico:
    def __init__(self, dados):
        self.id = dados['id']
        self.nome = dados['nome']
        self.area = dados['area']
        self.categoria = dados['categoria']
        self.descricao = dados['descricao']
        self.facilidadeUso = dados['facilidadeUso']
        self.engajamentoPotencial = dados['engajamentoPotencial']
        self.adaptabilidadePedagogica = dados['adaptabilidadePedagogica']
        self.requisitosInfraestrutura = dados['requisitosInfraestrutura']
        self.custoAcessibilidade = dados['custoAcessibilidade']
        self.tags = dados['tags']
        self.modalidades = dados['modalidades']
        self.dispositivos = dados['dispositivos']
        self.avaliacao = dados['avaliacao']
        self.offline = dados['offline']
        self.referencias = dados.get('referencias', [])
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'area': self.area,
            'categoria': self.categoria,
            'descricao': self.descricao,
            'facilidadeUso': self.facilidadeUso,
            'engajamentoPotencial': self.engajamentoPotencial,
            'adaptabilidadePedagogica': self.adaptabilidadePedagogica,
            'requisitosInfraestrutura': self.requisitosInfraestrutura,
            'custoAcessibilidade': self.custoAcessibilidade,
            'tags': self.tags,
            'modalidades': self.modalidades,
            'dispositivos': self.dispositivos,
            'avaliacao': self.avaliacao,
            'offline': self.offline,
            'referencias': self.referencias
        }

class RecursosRepository:
    def __init__(self):
        self.recursos = self._carregar_recursos()
    
    def _carregar_recursos(self):
        caminho = Path(__file__).parent.parent / 'data' / 'recursos_base.json'
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        return [RecursoTecnologico(r) for r in dados]
    
    def obter_todos(self):
        return self.recursos
    
    def obter_por_id(self, recurso_id):
        for recurso in self.recursos:
            if recurso.id == recurso_id:
                return recurso
        return None