import { Link, useNavigate } from "react-router-dom";
import { useAuthContext } from "../context/AuthContext";
import api from "../services/api";
import "./Navbar.css";

function Navbar() {
  const { user, logout } = useAuthContext();
  const navigate = useNavigate();

  const handleLogout = async () => {
  const refreshToken = localStorage.getItem("refresh_token");

  try {
    await api.post("/auth/logout", {
      refresh_token: refreshToken,
    });
  } catch {
    // ignore failure
  }

  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user");

  navigate("/login");
  };


  return (
    <nav>
      
      <Link to="/">
        <h3>Task Manager</h3>
      </Link>

      <ul>
        <li>
          <Link to="/">Dashboard</Link>
        </li>
        <li>
          <Link to="/tasks">Tasks</Link>
        </li>
      </ul>

      <div>
        <span>{user?.email}</span>
        <button onClick={handleLogout}>Logout</button>
      </div>
    </nav>
  );
}

export default Navbar;
