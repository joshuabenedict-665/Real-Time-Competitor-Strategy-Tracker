import React from "react";
import Card from "@mui/material/Card";
import CardMedia from "@mui/material/CardMedia";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import CardActions from "@mui/material/CardActions";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";

export default function ProductCard({ product, onAdd }) {
  return (
    <Card sx={{ width: 220, borderRadius: 2, boxShadow: 3 }}>
      <CardMedia
        component="img"
        height="140"
        image={product.imageUrl || "https://via.placeholder.com/220x140"}
        alt={product.name}
        sx={{ objectFit: "cover" }}
      />
      <CardContent>
        <Typography variant="subtitle1" noWrap sx={{ fontWeight: 700 }}>
          {product.name}
        </Typography>
        <Typography variant="body2" color="text.secondary" noWrap>
          {product.brand || "—"}
        </Typography>
        <Box sx={{ mt: 1 }}>
          <Typography variant="h6" sx={{ fontWeight: 800 }}>
            ₹{product.basePrice ?? product.price ?? "—"}
          </Typography>
        </Box>
      </CardContent>
      <CardActions>
        <Button size="small" onClick={() => onAdd?.(product)} variant="contained" sx={{ ml: 1 }}>
          Add to Cart
        </Button>
      </CardActions>
    </Card>
  );
}
