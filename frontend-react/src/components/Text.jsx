import './Text.css'

const VARIANT_TAGS = {
  body: 'p',
  caption: 'span',
  lead: 'p',
}

function Text({
  as,
  children,
  className = '',
  tone = 'default',
  variant = 'body',
  ...props
}) {
  const Component = as || VARIANT_TAGS[variant] || 'p'
  const classes = ['text', `text--${variant}`, `text--${tone}`, className]
    .filter(Boolean)
    .join(' ')

  return (
    <Component className={classes} {...props}>
      {children}
    </Component>
  )
}

export default Text
