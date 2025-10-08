import { useCart } from "../context/CartContext";

export default function ProductCard({ product }) {
  const { addToCart } = useCart();
  const imageSrc = product.image || "/placeholder.jpg";
  const productName = product.name || "Unnamed Product";
  const productPrice = product.current_price ?? 0;

  return (
    <div className="product-card bg-white rounded-xl overflow-hidden shadow-md hover:shadow-2xl transition duration-300 flex flex-col">
      <div className="relative">
        <img
          src={imageSrc}
          alt={productName}
          className="w-full h-56 object-cover"
        />
        <span className="absolute top-3 left-3 bg-emerald-500 text-white text-xs font-bold px-3 py-1 rounded-full">
          Bestseller
        </span>
      </div>
      <div className="p-4 flex flex-col flex-grow justify-between">
        <div>
          <h2 className="text-lg font-bold text-gray-800 truncate">
            {productName}
          </h2>
          <p className="text-amber-600 font-semibold mt-1 text-lg">
            ₹{productPrice}
          </p>
        </div>
        <button
          onClick={() =>
            addToCart({ ...product, price: product.current_price })
          }
          className="mt-4 bg-gradient-to-r from-emerald-500 to-teal-500 text-white py-2 rounded-lg hover:from-emerald-600 hover:to-teal-600 transition font-semibold shadow-md"
        >
          Add to Cart
        </button>
      </div>
    </div>
  );
}
