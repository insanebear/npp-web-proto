const Background = () => {
  return (
    <>
      {/* 왼쪽 검은색 메뉴 배경 */}
      <div 
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '300px',
          height: '300vh',
          backgroundColor: '#1f2937', // gray-800
          zIndex: -1
        }}
      />
      
      {/* 오른쪽 회색 메인 배경 */}
      <div 
        style={{
          position: 'absolute',
          top: 0,
          left: '300px',
          right: 0,
          height: '300vh',
          backgroundColor: '#e5e7eb', // gray-200
          zIndex: -1
        }}
      />
    </>
  );
}

export default Background;