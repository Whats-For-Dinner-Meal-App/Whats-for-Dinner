import "./SideBar.css";

function Sidebar({ title, isActive = true, body, styles }) {
  return (
    isActive && (
      <div className="sidebar-container" style={styles?.container}>
        <div className="sidebar-title" style={styles?.title}>
          {title}
        </div>
        <div className="sidebar-body" style={styles?.body}>
          {body}
        </div>
      </div>
    )
  );
}

export default Sidebar;
