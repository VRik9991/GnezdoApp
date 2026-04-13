import './Button.css'

function Button({ children, onClick, className = '', type = 'button' }) {
  return (
    <button
      type={type}
      onClick={onClick}
      className={`app-button ${className}`.trim()}
    >
      <span className="app-button__label">{children}</span>
    </button>
  )
}

export default Button
