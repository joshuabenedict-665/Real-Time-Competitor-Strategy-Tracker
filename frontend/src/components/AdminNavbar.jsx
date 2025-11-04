import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import { useNavigate } from "react-router-dom";
import AdminPanelSettingsIcon from "@mui/icons-material/AdminPanelSettings";

const AdminNavbar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/");
  };

  return (
    <AppBar position="static" elevation={3} sx={{ bgcolor: "#0f1724" }}>
      <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1, cursor: "pointer" }} onClick={() => navigate("/admin/dashboard")}>
          <AdminPanelSettingsIcon sx={{ transform: "scale(1.15)" }} />
          <Typography variant="h6" sx={{ fontWeight: 700 }}>
            ShopSmart Admin
          </Typography>
        </Box>

        <Box>
          <Button color="inherit" onClick={() => navigate("/admin/dashboard")}>
            Dashboard
          </Button>
          <Button color="inherit" onClick={() => navigate("/admin/dashboard")}>
            Scrape
          </Button>
          <Button
            variant="outlined"
            sx={{
              ml: 2,
              color: "#fff",
              borderColor: "rgba(255,255,255,0.25)",
            }}
            onClick={handleLogout}
          >
            Logout
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default AdminNavbar;
