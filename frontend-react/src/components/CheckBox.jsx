import './CheckBox.css'

function CheckBox({
  checked,
  onToggle,
  className = '',
  label = 'Toggle checkbox',
  disabled = false,
}) {
  return (
    <button
      type="button"
      aria-label={label}
      aria-pressed={checked}
      onClick={disabled ? undefined : onToggle}
      disabled={disabled}
      className={`check-box ${checked ? 'checked' : ''} ${className}`.trim()}
    >
      {checked ? '\u2705' : '\u274C'}
    </button>
  )
}

export default CheckBox
