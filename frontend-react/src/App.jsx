import { useState } from 'react'
import Text from './components/Text.jsx'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Text> 
        Hi Danjya!
      </Text>
    </>
  )
}

export default App
