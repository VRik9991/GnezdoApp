import { useState } from 'react'
import TextDropdown from './components/TextDropdown.jsx'
import Hint from './components/Hint.jsx'

function App() {
  const [currentButtonText, setCurrentButtonText] = useState('')

  return (
    <>
      <TextDropdown
        messages={[
  'Вот появился первый текст.',
  'Их тут несколько.',
  'А этот текст слишком огромный.',
  'Леша не токсичь',
]}
        onChange={setCurrentButtonText}
      />
      <Hint
        buttonLabel="Показать подсказку"
        title="Подсказка:"
        message="Тыкнув на пространство вне подсказки она закроется!"
      />
    </>
  )
}

export default App
