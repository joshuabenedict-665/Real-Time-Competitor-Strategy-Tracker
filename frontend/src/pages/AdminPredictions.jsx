import React, { useEffect, useState } from "react";
import API from "../api/api";
import AdminNavbar from "../components/AdminNavbar";
import {
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  CircularProgress,
  Typography,
} from "@mui/material";

const AdminPredictions = () => {
  const [loading, setLoading] = useState(true);
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    const fetchPredictedPrices = async () => {
      try {
        const { data } = await API.get("/admin/predictions");
        setPredictions(data.predictions || data.predictions || []);
      } catch (error) {
        console.error("Error fetching predictions", error);
      } finally {
        setLoading(false);
      }
    };
    fetchPredictedPrices();
  }, []);

  if (loading)
    return (
      <div style={{ textAlign: "center", marginTop: "50px" }}>
        <CircularProgress />
      </div>
    );

  return (
    <>
      <AdminNavbar />
      <Paper sx={{ margin: "20px", padding: "20px" }}>
        <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
          📊 Predicted Product Prices
        </Typography>

        <Table>
          <TableHead>
            <TableRow>
              <TableCell><strong>Product Name</strong></TableCell>
              <TableCell><strong>Base Price</strong></TableCell>
              <TableCell><strong>Predicted Price</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {predictions.map((item) => (
              <TableRow key={item.product_id}>
                <TableCell>{item.product_name}</TableCell>
                <TableCell>₹{item.base_price || "-"}</TableCell>
                <TableCell style={{ fontWeight: 700 }}>
                  ₹{item.predicted_price?.toFixed(2) || "N/A"}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>
    </>
  );
};

export default AdminPredictions;
