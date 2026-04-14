import './Sidebar.css'

function Sidebar({ activeTab, onSelectTab }) {
  return (
    <div className="sidebar-shell">
      <div className="sidebar-edge" />
      <aside className="sidebar-panel">
        <button
          className={activeTab === 'base' ? 'tab-button active' : 'tab-button'}
          onClick={() => onSelectTab('base')}
        >
          Base
        </button>
        <button
          className={activeTab === 'map' ? 'tab-button active' : 'tab-button'}
          onClick={() => onSelectTab('map')}
        >
          Map
        </button>
      </aside>
    </div>
  )
}

export default Sidebar
