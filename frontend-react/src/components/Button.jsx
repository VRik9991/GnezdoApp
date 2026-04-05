
import './Button.css'

function Button({ children, onClick, className = '', type = 'button' }) {
  return (
    <button
      type={type}
      onClick={onClick}
      className={`app-button ${className}`.trim()}
    >
      {children}
    </button>
  )
}

export default Button
