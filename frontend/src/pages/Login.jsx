import React, { useState } from "react";
import API from "../api/api";
import { useNavigate } from "react-router-dom";
import Container from "@mui/material/Container";
import Paper from "@mui/material/Paper";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await API.post("/auth/login", {
        username,
        password,
      });

      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("role", res.data.role);

      if (res.data.role === "admin") {
        navigate("/admin/dashboard");
      } else {
        navigate("/products");
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Invalid credentials");
      console.error("Login Error:", err);
    }
  };

  return (
    <Container maxWidth="xs" sx={{ mt: 10 }}>
      <Paper sx={{ p: 4 }}>
        <Typography variant="h5" sx={{ mb: 2 }}>Login</Typography>
        {error && <Typography color="error" sx={{ mb: 1 }}>{error}</Typography>}
        <Box component="form" onSubmit={handleLogin} sx={{ display: "grid", gap: 2 }}>
          <TextField label="Username" required value={username} onChange={(e) => setUsername(e.target.value)} />
          <TextField label="Password" type="password" required value={password} onChange={(e) => setPassword(e.target.value)} />
          <Button type="submit" variant="contained">Login</Button>
        </Box>

        <Typography sx={{ mt: 2, fontSize: 14 }}>
          Don’t have an account? <Button variant="text" onClick={() => navigate("/signup")}>Signup</Button>
        </Typography>
      </Paper>
    </Container>
  );
}
