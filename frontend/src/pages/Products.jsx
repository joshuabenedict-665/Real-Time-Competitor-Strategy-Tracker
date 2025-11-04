import React, { useEffect, useState } from "react";
import API from "../api/api";
import ProductCard from "../components/ProductCard";
import Navbar from "../components/Navbar";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import CircularProgress from "@mui/material/CircularProgress";

export default function Products() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const token = localStorage.getItem("token");

        if (!token) {
          setLoading(false);
          return;
        }

        const res = await API.get("/products/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setProducts(res.data.products || []);
      } catch (err) {
        console.error("Unauthorized / Error:", err);

        if (err.response?.status === 401 || err.response?.status === 403) {
          localStorage.removeItem("token");
          window.location.href = "/login";
        }
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const addToCart = (p) => alert(`Added ${p.name} to cart`);

  return (
    <div>
      <Navbar />
      <Container sx={{ mt: 3 }}>
        <Typography variant="h4" sx={{ mb: 2 }}>Products</Typography>

        {loading ? (
          <CircularProgress />
        ) : products.length === 0 ? (
          <Typography>No products available.</Typography>
        ) : (
          <Grid container spacing={2}>
            {products.map((p) => (
              <Grid item key={p._id}>
                <ProductCard product={p} onAdd={addToCart} />
              </Grid>
            ))}
          </Grid>
        )}
      </Container>
    </div>
  );
}
