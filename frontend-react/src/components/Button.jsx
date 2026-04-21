
import './Button.css'

function Button({
  children,
  onClick,
  className = '',
  type = 'button',
  disabled = false,
  ...props
}) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`app-button ${className}`.trim()}
      {...props}
    >
      {children}
    </button>
  )
}

export default Button
