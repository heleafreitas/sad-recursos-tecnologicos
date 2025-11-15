import { Award, BarChart3, CheckCircle, TrendingUp } from 'lucide-react';

const Resultado = ({ ranking, analises, onNovaConsulta }) => {
  const getCorMedalha = (idx) => {
    if (idx === 0) return 'bg-yellow-500';
    if (idx === 1) return 'bg-gray-400';
    if (idx === 2) return 'bg-orange-600';
    return 'bg-indigo-400';
  };

  return (
    <div className="space-y-6">
      {/* Análises Estatísticas */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg shadow-lg p-6 text-white">
        <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
          <BarChart3 size={28} />
          Análise do Sistema
        </h2>
        <div className="grid md:grid-cols-4 gap-4">
          <div className="bg-white bg-opacity-20 rounded-lg p-4">
            <p className="text-sm opacity-90">Recursos Analisados</p>
            <p className="text-3xl font-bold">{analises.totalRecursos}</p>
          </div>
          <div className="bg-white bg-opacity-20 rounded-lg p-4">
            <p className="text-sm opacity-90">Elegíveis</p>
            <p className="text-3xl font-bold">{analises.recursosElegiveis}</p>
          </div>
          <div className="bg-white bg-opacity-20 rounded-lg p-4">
            <p className="text-sm opacity-90">Taxa de Filtragem</p>
            <p className="text-3xl font-bold">{analises.taxaFiltragem}%</p>
          </div>
          <div className="bg-white bg-opacity-20 rounded-lg p-4">
            <p className="text-sm opacity-90">Critério Predominante</p>
            <p className="text-2xl font-bold">{analises.principalCriterio}</p>
          </div>
        </div>
      </div>

      {/* Ranking de Recomendações */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-indigo-900 mb-6 flex items-center gap-2">
          <Award size={28} />
          Top {ranking.length} Recursos Recomendados
        </h2>

        <div className="space-y-4">
          {ranking.map((recurso, idx) => (
            <div key={recurso.id} className="border-2 border-indigo-200 rounded-lg p-5 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-xl ${getCorMedalha(idx)}`}>
                    {idx + 1}
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-800">{recurso.nome}</h3>
                    <p className="text-sm text-gray-600">{recurso.categoria}</p>
                    <span className="inline-block mt-1 px-2 py-1 bg-indigo-100 text-indigo-700 text-xs rounded-full">
                      {recurso.area}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-indigo-600">{(recurso.scoreFinal * 100).toFixed(1)}%</p>
                  <p className="text-xs text-gray-500">Score Total</p>
                </div>
              </div>

              <p className="text-gray-700 mb-4">{recurso.descricao}</p>

              {/* Scores Detalhados */}
              <div className="grid md:grid-cols-3 gap-3 mb-4">
                <div className="bg-blue-50 p-3 rounded-lg">
                  <p className="text-xs text-blue-800 font-medium">Score Base</p>
                  <p className="text-lg font-bold text-blue-900">{(recurso.scoreBase * 100).toFixed(1)}%</p>
                  <p className="text-xs text-blue-600">Características intrínsecas</p>
                </div>
                <div className="bg-green-50 p-3 rounded-lg">
                  <p className="text-xs text-green-800 font-medium">Associação</p>
                  <p className="text-lg font-bold text-green-900">{(recurso.scoreAssociacao * 100).toFixed(1)}%</p>
                  <p className="text-xs text-green-600">Compatibilidade contextual</p>
                </div>
                <div className="bg-purple-50 p-3 rounded-lg">
                  <p className="text-xs text-purple-800 font-medium">Similaridade</p>
                  <p className="text-lg font-bold text-purple-900">{(recurso.scoreSimilaridade * 100).toFixed(1)}%</p>
                  <p className="text-xs text-purple-600">Alinhamento com perfil</p>
                </div>
              </div>

              {/* Características do Recurso */}
              <div className="grid grid-cols-5 gap-2 mb-4">
                {Object.entries(recurso.caracteristicas).map(([key, value]) => (
                  <div key={key} className="text-center">
                    <div className="w-full bg-gray-200 rounded-full h-2 mb-1">
                      <div 
                        className={`h-2 rounded-full ${value >= 0.8 ? 'bg-green-500' : value >= 0.6 ? 'bg-yellow-500' : 'bg-orange-500'}`}
                        style={{ width: `${value * 100}%` }}
                      ></div>
                    </div>
                    <p className="text-xs text-gray-600 truncate" title={key}>
                      {key.replace(/([A-Z])/g, ' $1').trim()}
                    </p>
                  </div>
                ))}
              </div>

              {/* Justificativa */}
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                  <TrendingUp size={16} />
                  Por que este recurso foi recomendado:
                </p>
                {recurso.regrasAtivadas && recurso.regrasAtivadas.length > 0 ? (
                  <ul className="space-y-1 text-sm text-gray-600">
                    {recurso.regrasAtivadas.map((regra, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <CheckCircle size={16} className="text-green-600 mt-0.5 flex-shrink-0" />
                        <span>{regra}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-gray-600">Recurso bem equilibrado para seu contexto</p>
                )}
              </div>

              {/* Referências */}
              {recurso.referencias && recurso.referencias.length > 0 && (
                <details className="mt-4">
                  <summary className="text-sm font-semibold text-indigo-700 cursor-pointer hover:text-indigo-900">
                    Ver referências bibliográficas ({recurso.referencias.length})
                  </summary>
                  <ul className="mt-2 space-y-1 pl-4">
                    {recurso.referencias.map((ref, i) => (
                      <li key={i} className="text-xs text-gray-600 border-l-2 border-gray-300 pl-2">
                        {ref}
                      </li>
                    ))}
                  </ul>
                </details>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Botão Nova Consulta */}
      <button
        onClick={onNovaConsulta}
        className="w-full py-3 bg-gray-600 text-white font-bold rounded-lg hover:bg-gray-700 transition"
      >
        Nova Consulta
      </button>
    </div>
  );
};

export default Resultado;