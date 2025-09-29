import { useCart } from "../context/CartContext";

export default function ProductCard({ product }) {
  const { addToCart } = useCart();

  return (
    <div className="product-card p-4 border rounded-xl shadow bg-white">
      <img
        src={product.image}
        alt={product.name}
        className="w-full h-40 object-cover rounded-md"
      />
      <h2 className="text-xl font-semibold mt-3">{product.name}</h2>
      <p className="text-green-600 font-medium mt-1">₹{product.price}</p>
      <button
        onClick={() => addToCart(product)}
        className="mt-4 w-full px-4 py-2 bg-indigo-500 text-white rounded hover:bg-indigo-600"
      >
        Add to Cart
      </button>
    </div>
  );
}
