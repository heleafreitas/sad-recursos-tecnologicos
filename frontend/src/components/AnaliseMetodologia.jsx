import { BookOpen, Code, TrendingUp } from 'lucide-react';
import { useEffect, useState } from 'react';
import { metodologiaService } from '../services/api';

const AnaliseMetodologia = () => {
  const [metodologia, setMetodologia] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    carregarMetodologia();
  }, []);

  const carregarMetodologia = async () => {
    try {
      const response = await metodologiaService.obter();
      setMetodologia(response.data);
    } catch (error) {
      console.error('Erro ao carregar metodologia:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <p className="text-gray-600">Carregando metodologia...</p>
      </div>
    );
  }

  if (!metodologia) {
    return null;
  }

  const cores = ['blue', 'green', 'purple'];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-indigo-900 mb-4 flex items-center gap-2">
        <BookOpen size={24} />
        Metodologia de Análise
      </h2>
      
      <div className="space-y-4">
        {metodologia.funcoes.map((funcao, idx) => (
          <div key={idx} className={`border-l-4 border-${cores[idx]}-500 pl-4 py-2`}>
            <h3 className={`font-bold text-${cores[idx]}-900 mb-2 flex items-center gap-2`}>
              {idx === 0 && <Code size={18} />}
              {idx === 1 && <TrendingUp size={18} />}
              {idx === 2 && <TrendingUp size={18} />}
              {idx + 1}. {funcao.nome}
            </h3>
            <p className="text-sm text-gray-700 mb-2">{funcao.descricao}</p>
            <div className="flex gap-4 text-xs text-gray-600">
              <span className="font-medium">📚 {funcao.biblioteca}</span>
              <span className="font-medium">⚖️ Peso: {funcao.peso}</span>
            </div>
          </div>
        ))}

        <div className="bg-indigo-50 p-4 rounded-lg mt-4">
          <h3 className="font-bold text-indigo-900 mb-2">Fórmula do Score Final</h3>
          <code className="text-sm bg-white p-2 rounded block">
            {metodologia.formula_score_final}
          </code>
        </div>
      </div>
    </div>
  );
};

export default AnaliseMetodologia;