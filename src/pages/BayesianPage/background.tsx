import Rectangle from "../../utilities/rectangle";

const Background = () => {
  return (
    <>
      <Rectangle
        width="300px"
        height="93.5%"
        color="bg-gray-800"
        center={{ x: '150px', y: '70%' }}
        shape="sharp-rectangle"
      />
      <Rectangle
        width="calc(100% - 300px)"
        height="93.5%"
        color="bg-gray-200"
        center={{ x: 'calc(50% + 150px)', y: '70%' }}
        shape="sharp-rectangle"
      />
    </>
  );
}
export default Background;