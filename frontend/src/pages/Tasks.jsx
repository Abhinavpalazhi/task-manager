import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import api from "../services/api";
import "./Tasks.css";

function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");

  // Fetch tasks
  useEffect(() => {
    api
      .get("/tasks")
      .then((res) => setTasks(res.data))
      .catch(() => alert("Unauthorized"));
  }, []);

  // Add task
  const handleAddTask = async (e) => {
    e.preventDefault();
    if (!newTask.trim()) return;

    const res = await api.post("/tasks", { title: newTask });
    setTasks([...tasks, res.data]);
    setNewTask("");
  };

  // Delete task
  const handleDeleteTask = async (id) => {
    await api.delete(`/tasks/${id}`);
    setTasks(tasks.filter((task) => task.id !== id));
  };

  // TOGGLE task (NEW)
  const handleToggleTask = async (id) => {
    const res = await api.patch(`/tasks/${id}`);

    setTasks(
      tasks.map((task) =>
        task.id === id
          ? { ...task, completed: res.data.completed }
          : task
      )
    );
  };

  return (
    <>
      <Navbar />

      <div className="tasks-container">
        <h2>Tasks</h2>

        <form onSubmit={handleAddTask}>
          <input
            placeholder="New task"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
          />
          <button type="submit">Add</button>
        </form>

        <ul>
          {tasks.map((task) => (
            <li key={task.id}>
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => handleToggleTask(task.id)}
              />

              <span
                style={{
                  marginLeft: "10px",
                  textDecoration: task.completed
                    ? "line-through"
                    : "none",
                }}
              >
                {task.title}
              </span>

              <button
                style={{ marginLeft: "10px" }}
                onClick={() => handleDeleteTask(task.id)}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}

export default Tasks;
