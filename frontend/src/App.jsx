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
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-2 md:p-4 lg:p-6">
      <div className="container mx-auto px-2">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-4 md:p-6 mb-6">
          <h2 className="text-2xl md:text-3xl font-bold text-indigo-900 mb-2">
            EdTech: Sistema de Apoio à Decisão para Recursos Tecnológicos
          </h2>
          <p className="text-gray-600 text-sm md:text-base">
            Recomendação personalizada baseada em análise de dados com Python
          </p>
          <div className="mt-3 flex flex-wrap gap-2 text-xs md:text-sm">
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
              <p className="text-red-800 font-medium text-sm md:text-base">{erro}</p>
            </div>
          </div>
        )}

        {/* Conteúdo */}
        {etapa === 'questionario' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <Questionario onSubmit={handleSubmitQuestionario} />
            </div>
            <div className="lg:col-span-1">
              <AnaliseMetodologia />
            </div>
          </div>
        )}

        {etapa === 'resultado' && resultado && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <Resultado 
                ranking={resultado.ranking} 
                analises={resultado.analises}
                onNovaConsulta={handleNovaConsulta}
              />
            </div>
            <div className="lg:col-span-1">
              <AnaliseMetodologia />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;