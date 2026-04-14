import { useState } from 'react'
import Button from './Button.jsx'
import Text from './Text.jsx'
import './Hint.css'

function Hint({
  buttonLabel,
  title,
  message,
}) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <section className="hint">
      <Button onClick={() => setIsOpen(true)}>{buttonLabel}</Button>

      {isOpen ? (
        <div
          className="hint__overlay"
          role="presentation"
          onClick={() => setIsOpen(false)}
        >
          <div
            className="hint__dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="hint-title"
            onClick={(event) => event.stopPropagation()}
          >
            <Text
              as="h2"
              variant="lead"
              tone="strong"
              className="hint__title"
              id="hint-title"
            >
              {title}
            </Text>
            <Text className="hint__message">{message}</Text>
          </div>
        </div>
      ) : null}
    </section>
  )
}

export default Hint
