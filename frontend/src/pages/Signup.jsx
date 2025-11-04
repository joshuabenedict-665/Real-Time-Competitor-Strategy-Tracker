import React, { useState } from "react";
import API from "../api/api";
import { useNavigate } from "react-router-dom";
import Container from "@mui/material/Container";
import Paper from "@mui/material/Paper";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import MenuItem from "@mui/material/MenuItem";
import Box from "@mui/material/Box";

export default function Signup() {
  const [form, setForm] = useState({ username: "", password: "", role: "user" });
  const navigate = useNavigate();

  const handleSubmit = async () => {
    try {
      await API.post("/auth/signup", form);
      alert("Account created successfully");
      navigate("/login");
    } catch (err) {
      alert(err.response?.data?.detail || "Signup failed!");
    }
  };

  return (
    <Container maxWidth="xs" sx={{ mt: 10 }}>
      <Paper sx={{ p: 4 }}>
        <Typography variant="h5" sx={{ mb: 2 }}>Create Account</Typography>

        <Box sx={{ display: "grid", gap: 2 }}>
          <TextField select label="Role" value={form.role} onChange={(e) => setForm({...form, role: e.target.value})}>
            <MenuItem value="user">User</MenuItem>
            <MenuItem value="admin">Admin</MenuItem>
          </TextField>

          <TextField label="Username" value={form.username} onChange={(e) => setForm({...form, username: e.target.value})} />
          <TextField label="Password" type="password" value={form.password} onChange={(e) => setForm({...form, password: e.target.value})} />
          <Button variant="contained" onClick={handleSubmit}>Sign Up</Button>
          <Button variant="text" onClick={() => navigate("/login")}>Already have an account? Login</Button>
        </Box>
      </Paper>
    </Container>
  );
}
