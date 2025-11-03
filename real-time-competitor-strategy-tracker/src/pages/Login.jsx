import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [msg, setMsg] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    const data = await res.json();

    if (res.ok) {
      setMsg("✅ Login successful!");
      localStorage.setItem("user", JSON.stringify(data.user));
      setTimeout(() => navigate("/products"), 1000);

    } else {
      setMsg(data.detail || "Login failed");
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gray-50">
      <h1 className="text-3xl font-bold mb-6">Login</h1>
      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-lg p-6 rounded-xl w-80"
      >
        <input
          type="text"
          placeholder="Username"
          className="w-full p-3 border mb-3 rounded"
          onChange={(e) => setForm({ ...form, username: e.target.value })}
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full p-3 border mb-3 rounded"
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        <button className="w-full bg-amber-500 text-white py-2 rounded hover:bg-amber-600">
          Login
        </button>
      </form>
      {msg && <p className="mt-4 text-gray-700">{msg}</p>}

      <p className="mt-4 text-sm text-gray-600">
        Don’t have an account?{" "}
        <a href="/signup" className="text-amber-600 hover:underline">
          Sign Up
        </a>
      </p>
    </div>
  );
}
