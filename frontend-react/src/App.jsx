import { useState } from 'react'
import './App.css'
import Sidebar from './components/Sidebar'
import Button from './components/Button'
import CheckBox from './components/CheckBox'

function App() {
  const [activeTab, setActiveTab] = useState('base')
  const [count, setCount] = useState(0)
  const [isChecked, setIsChecked] = useState(false)

  return (
    <>
      <Sidebar activeTab={activeTab} onSelectTab={setActiveTab} />

      <main className={activeTab === 'base' ? 'page-shell page-shell-base' : 'page-shell'}>
        {activeTab === 'base' && (
          <section className="home-panel">
            <p className="eyebrow">Gnezdo</p>
            <h1>Main Page</h1>
            <Button
              onClick={() => setCount((count) => count + 1)}
            >
              Count is {count}
            </Button>

          </section>
        )}

        {activeTab === 'map' && (
  <>
    <section className="content-panel">
      <h1>Map Page</h1>
    </section>
    <CheckBox
      checked={isChecked}
      onToggle={() => setIsChecked((currentValue) => !currentValue)}
      label="Main page checkbox"
    />
  </>
)}
      </main>
    </>
  )
}

export default App
