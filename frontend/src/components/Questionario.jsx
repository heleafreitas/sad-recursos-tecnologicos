import { BookOpen, Check, ChevronLeft, ChevronRight, Settings, Users } from 'lucide-react';
import { useState } from 'react';

const Questionario = ({ onSubmit }) => {
  const [respostas, setRespostas] = useState({});
  const [loading, setLoading] = useState(false);
  const [etapaAtual, setEtapaAtual] = useState(0);

  const questionario = {
    perfilProfessor: [
      {
        id: 'disciplina',
        pergunta: 'Qual disciplina você leciona?',
        tipo: 'select',
        opcoes: ['Matemática', 'Redação', 'Física', 'Química', 'Biologia', 'História', 'Geografia', 'Multidisciplinar']
      },
      {
        id: 'familiaridadeTech',
        pergunta: 'Como você avalia seu nível de familiaridade com tecnologias educacionais?',
        tipo: 'radio',
        opcoes: [
          { valor: 0.3, label: 'Básico - Uso apenas ferramentas muito simples' },
          { valor: 0.6, label: 'Intermediário - Confortável com a maioria das tecnologias' },
          { valor: 0.9, label: 'Avançado - Consigo aprender novas ferramentas rapidamente' }
        ]
      },
      {
        id: 'estiloEnsino',
        pergunta: 'Qual seu estilo de ensino predominante?',
        tipo: 'radio',
        opcoes: [
          { valor: 'expositivo', label: 'Expositivo - Aulas teóricas e demonstrações' },
          { valor: 'investigativo', label: 'Investigativo - Alunos exploram e descobrem' },
          { valor: 'projetos', label: 'Baseado em projetos - Trabalhos práticos e colaborativos' },
          { valor: 'hibrido', label: 'Híbrido - Combino diferentes metodologias' }
        ]
      },
      {
        id: 'objetivoAula',
        pergunta: 'Qual o principal objetivo desta aula?',
        tipo: 'radio',
        opcoes: [
          { valor: 'introducao', label: 'Introdução de novo conteúdo' },
          { valor: 'pratica', label: 'Prática e aplicação de conhecimentos' },
          { valor: 'revisao', label: 'Revisão para avaliações' },
          { valor: 'autonomia', label: 'Estímulo à autonomia e aprendizagem independente' }
        ]
      },
      {
        id: 'tempoPreparacao',
        pergunta: 'Quanto tempo você tem para preparar e aplicar este recurso?',
        tipo: 'radio',
        opcoes: [
          { valor: 0.3, label: 'Baixo - Menos de 30 minutos' },
          { valor: 0.6, label: 'Médio - 30 minutos a 2 horas' },
          { valor: 0.9, label: 'Alto - Mais de 2 horas' }
        ]
      }
    ],
    perfilTurma: [
      {
        id: 'tamanhoTurma',
        pergunta: 'Quantos alunos tem a turma?',
        tipo: 'number',
        placeholder: 'Ex: 35'
      },
      {
        id: 'engajamento',
        pergunta: 'Como você avalia o engajamento médio dos alunos?',
        tipo: 'radio',
        opcoes: [
          { valor: 0.3, label: 'Baixo - Turma desinteressada e dispersa' },
          { valor: 0.6, label: 'Médio - Participação moderada' },
          { valor: 0.9, label: 'Alto - Turma participativa e interessada' }
        ]
      },
      {
        id: 'acessoDispositivos',
        pergunta: 'Os alunos têm acesso a quais dispositivos?',
        tipo: 'checkbox',
        opcoes: [
          { valor: 'celular', label: 'Celular/Smartphone' },
          { valor: 'computador', label: 'Computador/Notebook' },
          { valor: 'nenhum', label: 'Nenhum dispositivo próprio' }
        ]
      },
      {
        id: 'conectividade',
        pergunta: 'Qual o nível de conectividade disponível?',
        tipo: 'radio',
        opcoes: [
          { valor: 0.2, label: 'Sem internet - Apenas offline' },
          { valor: 0.5, label: '3G/4G - Conexão móvel limitada' },
          { valor: 0.9, label: 'Wi-Fi - Conexão estável e rápida' }
        ]
      },
      {
        id: 'desempenho',
        pergunta: 'Como é o desempenho médio da turma na disciplina?',
        tipo: 'radio',
        opcoes: [
          { valor: 0.3, label: 'Baixo - Muitos alunos com dificuldades' },
          { valor: 0.6, label: 'Médio - Desempenho satisfatório' },
          { valor: 0.9, label: 'Alto - Maioria com bom desempenho' }
        ]
      }
    ],
    contextoPedagogico: [
      {
        id: 'modalidade',
        pergunta: 'Qual a modalidade da aula?',
        tipo: 'radio',
        opcoes: [
          { valor: 'presencial', label: 'Presencial' },
          { valor: 'hibrida', label: 'Híbrida (parte presencial, parte remota)' },
          { valor: 'remota', label: 'Totalmente remota' }
        ]
      },
      {
        id: 'tempoAula',
        pergunta: 'Quanto tempo de aula você tem disponível?',
        tipo: 'radio',
        opcoes: [
          { valor: 0.4, label: 'Curto - Até 50 minutos' },
          { valor: 0.7, label: 'Médio - 50 a 100 minutos' },
          { valor: 1.0, label: 'Longo - Mais de 100 minutos' }
        ]
      },
      {
        id: 'necessidadeAvaliacao',
        pergunta: 'Você precisa de feedback automático ou avaliação dos alunos?',
        tipo: 'radio',
        opcoes: [
          { valor: true, label: 'Sim, preciso acompanhar o desempenho individual' },
          { valor: false, label: 'Não, apenas atividade de aprendizagem' }
        ]
      },
      {
        id: 'infraestrutura',
        pergunta: 'Quais recursos de infraestrutura a escola possui?',
        tipo: 'checkbox',
        opcoes: [
          { valor: 'laboratorio', label: 'Laboratório de informática' },
          { valor: 'projetor', label: 'Projetor/TV' },
          { valor: 'wifi', label: 'Rede Wi-Fi para alunos' },
          { valor: 'nenhum', label: 'Recursos limitados' }
        ]
      }
    ]
  };

  const secoes = [
    { titulo: 'Perfil do Professor', icon: Users, perguntas: questionario.perfilProfessor },
    { titulo: 'Perfil da Turma', icon: BookOpen, perguntas: questionario.perfilTurma },
    { titulo: 'Contexto Pedagógico', icon: Settings, perguntas: questionario.contextoPedagogico }
  ];

  const handleResposta = (id, valor) => {
    setRespostas(prev => ({
      ...prev,
      [id]: valor
    }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      await onSubmit(respostas);
    } catch (error) {
      console.error('Erro ao submeter:', error);
    } finally {
      setLoading(false);
    }
  };

  const proximaEtapa = () => {
    if (etapaAtual < secoes.length - 1) {
      setEtapaAtual(etapaAtual + 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const etapaAnterior = () => {
    if (etapaAtual > 0) {
      setEtapaAtual(etapaAtual - 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const renderCampo = (pergunta) => {
    switch (pergunta.tipo) {
      case 'select':
        return (
          <select
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            onChange={(e) => handleResposta(pergunta.id, e.target.value)}
            value={respostas[pergunta.id] || ''}
          >
            <option value="">Selecione...</option>
            {pergunta.opcoes.map((op, i) => (
              <option key={i} value={op}>{op}</option>
            ))}
          </select>
        );

      case 'radio':
        return (
          <div className="space-y-2">
            {pergunta.opcoes.map((op, i) => (
              <label key={i} className="flex items-center p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition">
                <input
                  type="radio"
                  name={pergunta.id}
                  value={op.valor}
                  onChange={() => handleResposta(pergunta.id, op.valor)}
                  checked={respostas[pergunta.id] === op.valor}
                  className="mr-3 w-4 h-4 text-indigo-600"
                />
                <span className="text-gray-700">{op.label}</span>
              </label>
            ))}
          </div>
        );

      case 'checkbox':
        return (
          <div className="space-y-2">
            {pergunta.opcoes.map((op, i) => (
              <label key={i} className="flex items-center p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition">
                <input
                  type="checkbox"
                  value={op.valor}
                  onChange={(e) => {
                    const atual = respostas[pergunta.id] || [];
                    const novo = e.target.checked
                      ? [...atual, op.valor]
                      : atual.filter(v => v !== op.valor);
                    handleResposta(pergunta.id, novo);
                  }}
                  checked={(respostas[pergunta.id] || []).includes(op.valor)}
                  className="mr-3 w-4 h-4 text-indigo-600"
                />
                <span className="text-gray-700">{op.label}</span>
              </label>
            ))}
          </div>
        );

      case 'number':
        return (
          <input
            type="number"
            placeholder={pergunta.placeholder}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            onChange={(e) => handleResposta(pergunta.id, parseInt(e.target.value))}
            value={respostas[pergunta.id] || ''}
          />
        );

      default:
        return null;
    }
  };

  // Verifica se todos os campos da etapa atual estão preenchidos
  const etapaCompleta = () => {
    const perguntasEtapa = secoes[etapaAtual].perguntas;
    return perguntasEtapa.every(pergunta => {
      const resposta = respostas[pergunta.id];
      
      // Para checkboxes, verifica se pelo menos um foi selecionado
      if (pergunta.tipo === 'checkbox') {
        return resposta && resposta.length > 0;
      }
      
      // Para outros tipos, verifica se não está vazio/undefined/null
      return resposta !== undefined && resposta !== null && resposta !== '';
    });
  };

  // Verifica se todas as etapas estão completas
  const todasEtapasCompletas = () => {
    return secoes.every((secao) => {
      return secao.perguntas.every(pergunta => {
        const resposta = respostas[pergunta.id];
        if (pergunta.tipo === 'checkbox') {
          return resposta && resposta.length > 0;
        }
        return resposta !== undefined && resposta !== null && resposta !== '';
      });
    });
  };

  const secaoAtual = secoes[etapaAtual];
  const Icon = secaoAtual.icon;
  const ehUltimaEtapa = etapaAtual === secoes.length - 1;
  const podeAvancar = etapaCompleta();

  return (
    <div className="space-y-8">
      {/* Conteúdo da Etapa Atual */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div
            className="bg-indigo-600 h-2.5 rounded-full transition-all duration-300"
            style={{ width: `${((etapaAtual + 1) / secoes.length) * 100}%` }}
          ></div>
        </div>
        <h2 className="text-2xl font-bold text-indigo-900 mb-6 flex items-center gap-2 mt-4">
          <Icon size={24} />
          {secaoAtual.titulo}
        </h2>
        
        <div className="h-115 overflow-y-auto space-y-6">
          {secaoAtual.perguntas.map((pergunta) => (
            <div key={pergunta.id} className="border-b border-gray-200 pb-4 last:border-b-0">
              <label className="block text-gray-800 font-medium mb-3">
                {pergunta.pergunta}
                <span className="text-red-500 ml-1">*</span>
              </label>
              {renderCampo(pergunta)}
            </div>
          ))}
        </div>
      </div>

      {/* Botões de Navegação */}
      <div className="flex gap-4">
        <button
          onClick={etapaAnterior}
          disabled={etapaAtual === 0}
          className="flex-1 py-4 bg-gray-200 text-gray-700 font-bold rounded-lg hover:bg-gray-300 disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-lg transition"
        >
          <ChevronLeft size={24} />
          Anterior
        </button>

        {ehUltimaEtapa ? (
          <button
            onClick={handleSubmit}
            disabled={loading || !todasEtapasCompletas()}
            className="flex-1 py-4 bg-green-600 text-white font-bold rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-lg transition"
          >
            {loading ? 'Processando...' : 'Gerar Recomendações'}
            {!loading && <Check size={24} />}
          </button>
        ) : (
          <button
            onClick={proximaEtapa}
            disabled={!podeAvancar}
            className="flex-1 py-4 bg-indigo-600 text-white font-bold rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-lg transition"
          >
            Próxima
            <ChevronRight size={24} />
          </button>
        )}
      </div>
    </div>
  );
};

export default Questionario;