import axios from "axios";

const API_BASE = "http://127.0.0.1:8000"; // FastAPI backend URL

export const fetchProducts = async () => {
  try {
    const res = await axios.get(`${API_BASE}/products`);
    return res.data; // array of products
  } catch (err) {
    console.error("Error fetching products:", err);
    return [];
  }
};
