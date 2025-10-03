import { useEffect, useState } from "react";
import ProductCard from "../components/ProductCard";
import { fetchProducts } from "../api/api"; // API call to backend

const API_BASE = "http://localhost:8000"; // Your FastAPI backend URL

export default function Products() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts()
      .then((data) => setProducts(data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="p-8 text-center text-gray-500">
        Loading products...
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-6 p-8">
      {products.length === 0 ? (
        <p className="col-span-full text-center text-gray-500">
          No products available.
        </p>
      ) : (
        products.map((product, index) => (
          <ProductCard
            key={index}
            product={{
              ...product,
              image: `${API_BASE}${product.image}`, // fix image path
            }}
          />
        ))
      )}
    </div>
  );
}
