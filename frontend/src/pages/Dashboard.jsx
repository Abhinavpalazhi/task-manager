import Navbar from "../components/Navbar";
import { useAuthContext } from "../context/AuthContext";

function Dashboard() {
  const { user } = useAuthContext();

  return (
    <>
      <Navbar />

      <div>
        <h2>Dashboard</h2>
        <p>Welcome, {user?.email}</p>
      </div>
    </>
  );
}

export default Dashboard;
