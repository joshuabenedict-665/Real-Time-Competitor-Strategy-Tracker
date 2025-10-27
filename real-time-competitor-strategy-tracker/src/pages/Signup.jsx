import { useState } from "react";

export default function Signup() {
  const [form, setForm] = useState({ username: "", password: "", role: "user" });
  const [msg, setMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch("http://127.0.0.1:8000/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    const data = await res.json();
    setMsg(data.message || data.detail);
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gray-50">
      <h1 className="text-3xl font-bold mb-6">Create Account</h1>
      <form onSubmit={handleSubmit} className="bg-white shadow-lg p-6 rounded-xl w-80">
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
        <select
          className="w-full p-3 border mb-3 rounded"
          onChange={(e) => setForm({ ...form, role: e.target.value })}
        >
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
        <button className="w-full bg-amber-500 text-white py-2 rounded hover:bg-amber-600">
          Sign Up
        </button>
      </form>
      {msg && <p className="mt-4 text-gray-700">{msg}</p>}
    </div>
  );
}
