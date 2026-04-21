import './Sidebar.css'

const DEFAULT_TABS = [
  { id: 'base', label: 'Base' },
  { id: 'map', label: 'Map' },
]

function Sidebar({ activeTab, onSelectTab, tabs = DEFAULT_TABS, title = 'Gnezdo' }) {
  return (
    <div className="sidebar-shell">
      <div className="sidebar-edge" />
      <aside className="sidebar-panel">
        <p className="sidebar-title">{title}</p>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={activeTab === tab.id ? 'tab-button active' : 'tab-button'}
            onClick={() => onSelectTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </aside>
    </div>
  )
}

export default Sidebar
