import { useState } from 'react'
import Button from './Button.jsx'
import Text from './Text.jsx'
import './TextDropdown.css'

function TextDropdown({ onChange, messages }) {
  const [isVisible, setIsVisible] = useState(false)
  const [selectedMessage, setSelectedMessage] = useState('')

  function handleSelectMessage(message) {
    setSelectedMessage(message)
    setIsVisible(false)
    onChange?.(message)
  }

  return (
    <main className="toggle-text-shell">
      <div className="toggle-launcher">
        <Button
          className="toggle-launcher__button"
          onClick={() => setIsVisible(!isVisible)}
        >
          {selectedMessage}
        </Button>
        <div className={`toggle-text-panel ${isVisible ? 'is-visible' : ''}`.trim()}>
          <div className="toggle-text-list">
            {messages.map((message, index) => (
              <Button
                key={index}
                className="toggle-text-item"
                onClick={() => handleSelectMessage(message)}
              >
                <Text className="toggle-text-message" tone="strong">
                  {message}
                </Text>
              </Button>
            ))}
          </div>
        </div>
      </div>
    </main>
  )
}

export default TextDropdown
