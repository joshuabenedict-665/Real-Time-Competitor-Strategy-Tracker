import { useCart } from "../context/CartContext";

export default function ProductCard({ product }) {
  const { addToCart } = useCart();

  // Fallbacks for missing data from backend
  const imageSrc = product.image || "/placeholder.jpg";   // already full path from backend
  const productName = product.name || "Unnamed Product";
  const productPrice = product.current_price ?? 0;        // changed from 'price' to 'current_price'

  return (
    <div className="product-card p-4 border rounded-xl shadow bg-white">
      <img
        src={imageSrc}
        alt={productName}
        className="w-full h-40 object-cover rounded-md"
      />
      <h2 className="text-xl font-semibold mt-3">{productName}</h2>
      <p className="text-green-600 font-medium mt-1">₹{productPrice}</p>
      <button
  onClick={() => addToCart({
    ...product,
    price: product.current_price // map backend price to 'price'
  })}
  className="mt-4 w-full px-4 py-2 bg-indigo-500 text-white rounded hover:bg-indigo-600"
>
  Add to Cart
</button>

    </div>
  );
}
