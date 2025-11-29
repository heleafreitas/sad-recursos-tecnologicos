import { Award, BarChart3, CheckCircle, TrendingUp } from 'lucide-react';

function formatKey(key) {
    let separated = key.replace(/([A-Z])/g, ' $1').trim();
    return separated.charAt(0).toUpperCase() + separated.slice(1);
}

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
        <div className="grid md:grid-cols-3 gap-3">
          <div className="bg-white/10 rounded-lg p-4">
            <p className="text-sm opacity-90">Recursos Analisados</p>
            <p className="text-3xl font-bold">{analises.totalRecursos}</p>
          </div>
          <div className="bg-white/10 rounded-lg p-4">
            <p className="text-sm opacity-90">Elegíveis</p>
            <p className="text-3xl font-bold">{analises.recursosElegiveis}</p>
          </div>
          <div className="bg-white/10 rounded-lg p-4">
            <p className="text-sm opacity-90">Taxa de Filtragem</p>
            <p className="text-3xl font-bold">{analises.taxaFiltragem}%</p>
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
              {/* Características do Recurso */}
              <div className="grid grid-cols-5 gap-2 mb-4">
                {Object.entries(recurso.caracteristicas).map(([key, value]) => (
                  <div  key={key} className="flex flex-col justify-between bg-purple-50 p-3 rounded-lg">
                  <p className="text-xs text-purple-800 font-medium">{formatKey(key)}</p>
                  <p className="text-lg font-bold text-purple-900">{(value * 100).toFixed(1)}%</p>
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