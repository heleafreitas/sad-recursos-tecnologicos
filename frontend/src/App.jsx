import { AlertCircle } from 'lucide-react';
import { useState } from 'react';
import AnaliseMetodologia from './components/AnaliseMetodologia';
import Questionario from './components/Questionario';
import Resultado from './components/Resultado';
import { recomendacoesService } from './services/api';

function App() {
  const [etapa, setEtapa] = useState('questionario');
  const [resultado, setResultado] = useState(null);
  const [erro, setErro] = useState(null);

  const handleSubmitQuestionario = async (respostas) => {
    try {
      setErro(null);
      const response = await recomendacoesService.gerar(respostas);
      
      if (response.success) {
        setResultado(response.data);
        setEtapa('resultado');
      } else {
        setErro(response.error || 'Erro ao gerar recomendações');
      }
    } catch (error) {
      console.error('Erro:', error);
      setErro(
        error.response?.data?.error || 
        'Erro ao conectar com o servidor. Verifique se o backend está rodando.'
      );
    }
  };

  const handleNovaConsulta = () => {
    setEtapa('questionario');
    setResultado(null);
    setErro(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h1 className="text-3xl font-bold text-indigo-900 mb-2">
            Sistema de Apoio à Decisão para Recursos Tecnológicos
          </h1>
          <p className="text-gray-600">
            Recomendação personalizada baseada em análise de dados com Python
          </p>
          <div className="mt-3 flex gap-2 text-sm">
            <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full">React + Vite</span>
            <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full">Python + Flask</span>
            <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full">Scikit-learn</span>
          </div>
        </div>

        {/* Erro */}
        {erro && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded-lg">
            <div className="flex items-center gap-2">
              <AlertCircle className="text-red-600" size={20} />
              <p className="text-red-800 font-medium">{erro}</p>
            </div>
          </div>
        )}

        {/* Conteúdo */}
        {etapa === 'questionario' && (
          <>
            <Questionario onSubmit={handleSubmitQuestionario} />
            <div className="mt-6">
              <AnaliseMetodologia />
            </div>
          </>
        )}

        {etapa === 'resultado' && resultado && (
          <>
            <Resultado 
              ranking={resultado.ranking} 
              analises={resultado.analises}
              onNovaConsulta={handleNovaConsulta}
            />
            <div className="mt-6">
              <AnaliseMetodologia />
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;