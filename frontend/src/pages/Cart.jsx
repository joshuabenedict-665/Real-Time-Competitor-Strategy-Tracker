import React, { useEffect, useState } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import Container from "@mui/material/Container";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import Avatar from "@mui/material/Avatar";

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchCart = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) return;

      const res = await axios.get("http://127.0.0.1:8000/user/cart", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setCartItems(res.data);
      setLoading(false);
    } catch (error) {
      console.error("Cart Fetch Failed:", error);
      setLoading(false);
    }
  };

  const removeItem = async (productId) => {
    try {
      const token = localStorage.getItem("token");
      await axios.delete(`http://127.0.0.1:8000/user/cart/remove/${productId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setCartItems(cartItems.filter((item) => item._id !== productId));
    } catch (error) {
      console.error("Remove Failed:", error);
    }
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const totalPrice = cartItems
    .reduce((sum, item) => sum + Number(item.price || 0), 0)
    .toFixed(2);

  return (
    <div>
      <Navbar />
      <Container sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom align="center">Your Cart</Typography>

        {loading ? (
          <Typography align="center">Loading...</Typography>
        ) : cartItems.length === 0 ? (
          <Typography align="center">Your cart is empty</Typography>
        ) : (
          <Box sx={{ display: "grid", gap: 2 }}>
            {cartItems.map((item) => (
              <Paper key={item._id} sx={{ display: "flex", justifyContent: "space-between", p: 2, alignItems: "center" }}>
                <Box sx={{ display: "flex", gap: 2, alignItems: "center" }}>
                  <Avatar variant="rounded" src={item.image || "https://via.placeholder.com/100"} sx={{ width: 100, height: 100 }} />
                  <Box>
                    <Typography variant="h6">{item.name}</Typography>
                    <Typography color="text.secondary">₹{item.price}</Typography>
                  </Box>
                </Box>

                <Button variant="contained" color="error" onClick={() => removeItem(item._id)}>Remove</Button>
              </Paper>
            ))}

            <Paper sx={{ p: 2, textAlign: "right" }}>
              <Typography variant="h6">Total: ₹ {totalPrice}</Typography>
            </Paper>
          </Box>
        )}
      </Container>
    </div>
  );
};

export default Cart;
