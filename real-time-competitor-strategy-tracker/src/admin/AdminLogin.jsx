import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function AdminLogin() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [err, setErr] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErr("");
    try {
      const res = await fetch("http://localhost:8000/auth/admin-login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const json = await res.json();
      if (!res.ok) {
        setErr(json.detail || "Admin login failed");
        return;
      }
      // store token + role
      localStorage.setItem("token", json.access_token || json.access_token || json.access_token || json.get?.("access_token") || json.access_token || json.token || json.access_token || json.access_token);
      // robust: prefer 'access_token' then 'token'
      const tok = json.access_token || json.token;
      localStorage.setItem("token", tok);
      localStorage.setItem("role", "admin");
      navigate("/admin/dashboard");
    } catch (err) {
      setErr("Server error");
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h2 className="text-2xl mb-4">Admin Login</h2>
      {err && <div className="text-red-600 mb-3">{err}</div>}
      <form onSubmit={handleSubmit} className="space-y-3">
        <input name="username" placeholder="username" value={form.username} onChange={handleChange} className="w-full p-2 border rounded" />
        <input name="password" type="password" placeholder="password" value={form.password} onChange={handleChange} className="w-full p-2 border rounded" />
        <button className="w-full bg-amber-500 text-white p-2 rounded">Login</button>
      </form>
    </div>
  );
}
