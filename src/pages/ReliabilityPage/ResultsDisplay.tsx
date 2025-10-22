// FILE: src/pages/ReliabilityPage/ResultsDisplay.tsx

import React from 'react';

interface ResultsDisplayProps {
  results: object;
  onReset: () => void;
  simulationInput: object | null;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ results, onReset, simulationInput }) => {

  const handleSaveResults = () => {
    if (!results) {
      alert("No results to save.");
      return;
    }

    const combinedData = {
      input: simulationInput,
      output: results,
    };

    const jsonString = JSON.stringify(combinedData, null, 2);
    const blob = new Blob([jsonString], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    a.download = `simulation-results-${timestamp}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // 결과 데이터를 더 보기 좋게 표시하는 함수
  // const renderResults = () => {
  //   if (!results) return null;

  //   // Bayesian 시뮬레이션 결과인지 확인
  //   if (results.PFD || results.SR_Total_Remained_Defect) {
  //     return (
  //       <div className="space-y-4">
  //         <h3 className="text-lg font-semibold text-blue-800">Bayesian Simulation Results</h3>
          
  //         {/* 주요 파라미터들 표시 */}
  //         <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  //           {Object.entries(results).map(([param, data]: [string, any]) => (
  //             <div key={param} className="bg-blue-50 p-4 rounded-lg border">
  //               <h4 className="font-medium text-blue-900 mb-2">{param}</h4>
  //               <div className="space-y-1 text-sm">
  //                 <div className="flex justify-between">
  //                   <span>Mean:</span>
  //                   <span className="font-mono">{data.mean?.toFixed(6) || 'N/A'}</span>
  //                 </div>
  //                 <div className="flex justify-between">
  //                   <span>SD:</span>
  //                   <span className="font-mono">{data.sd?.toFixed(6) || 'N/A'}</span>
  //                 </div>
  //                 <div className="flex justify-between">
  //                   <span>Median:</span>
  //                   <span className="font-mono">{data.median?.toFixed(6) || 'N/A'}</span>
  //                 </div>
  //                 <div className="flex justify-between">
  //                   <span>95% CI:</span>
  //                   <span className="font-mono text-xs">
  //                     [{data.q2_5?.toFixed(6) || 'N/A'}, {data.q97_5?.toFixed(6) || 'N/A'}]
  //                   </span>
  //                 </div>
  //               </div>
  //             </div>
  //           ))}
  //         </div>
          
  //         {/* 전체 JSON 데이터 보기 토글 */}
  //         <details className="mt-4">
  //           <summary className="cursor-pointer text-sm text-gray-600 hover:text-gray-800">
  //             View Raw JSON Data
  //           </summary>
  //           <pre className="mt-2 bg-gray-100 p-4 rounded-md overflow-auto text-xs">
  //             {JSON.stringify(results, null, 2)}
  //           </pre>
  //         </details>
  //       </div>
  //     );
  //   }

  //   // 기존 형식의 결과 (통계적 분석 결과)
  //   return (
  //     <pre className="flex-grow bg-gray-100 p-4 rounded-md overflow-auto text-sm">
  //       {JSON.stringify(results, null, 2)}
  //     </pre>
  //   );
  // };
  const renderResults = () => {
    if (!results) return null;

    // Bayesian 시뮬레이션 결과인지 확인
    if (results.PFD || results.SR_Total_Remained_Defect) {
      return (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-blue-800">Bayesian Simulation Results</h3>
          
          {/* 주요 파라미터들 표시 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(results)
              .sort(([paramA], [paramB]) => {
                if (paramA === 'PFD') return -1; // PFD 항목을 배열의 맨 앞으로 보냅니다.
                if (paramB === 'PFD') return 1;  // paramB가 PFD면 paramA를 뒤로 보냅니다.
                return paramA.localeCompare(paramB); // 나머지 항목들은 알파벳순으로 정렬합니다.
              })
              .map(([param, data]: [string, any]) => (
              <div key={param} className="bg-blue-50 p-4 rounded-lg border">
                <h4 className="font-medium text-blue-900 mb-2">{param}</h4>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span>Mean:</span>
                    <span className="font-mono">{data.mean?.toFixed(6) || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>SD:</span>
                    <span className="font-mono">{data.sd?.toFixed(6) || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Median:</span>
                    <span className="font-mono">{data.median?.toFixed(6) || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>95% CI:</span>
                    <span className="font-mono text-xs">
                      [{data.q2_5?.toFixed(6) || 'N/A'}, {data.q97_5?.toFixed(6) || 'N/A'}]
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          {/* 전체 JSON 데이터 보기 토글 */}
          <details className="mt-4">
            <summary className="cursor-pointer text-sm text-gray-600 hover:text-gray-800">
              View Raw JSON Data
            </summary>
            <pre className="mt-2 bg-gray-100 p-4 rounded-md overflow-auto text-xs">
              {JSON.stringify(results, null, 2)}
            </pre>
          </details>
        </div>
      );
    }

    // 기존 형식의 결과 (통계적 분석 결과)
    return (
      <pre className="flex-grow bg-gray-100 p-4 rounded-md overflow-auto text-sm">
        {JSON.stringify(results, null, 2)}
      </pre>
    );
  };

  return (
    <div
      className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 p-6 bg-white rounded-lg shadow-2xl text-gray-800"
      style={{ width: '90%', maxWidth: '1200px', height: '85%', display: 'flex', flexDirection: 'column' }}
    >
      <h2 className="text-2xl font-bold mb-4 text-center">Simulation Results</h2>
      <div className="flex-grow overflow-auto">
        {renderResults()}
      </div>
      <div className="mt-4 flex justify-center items-center gap-4">
        <button
          onClick={handleSaveResults}
          className="px-6 py-2 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-500 transition-colors"
          title="Save input and output to a JSON file"
        >
          Save Results
        </button>
        <button
          onClick={onReset}
          className="px-6 py-2 bg-sky-600 text-white font-semibold rounded-lg hover:bg-sky-500 transition-colors"
        >
          Start New Simulation
        </button>
      </div>
    </div>
  );
};

export default ResultsDisplay;