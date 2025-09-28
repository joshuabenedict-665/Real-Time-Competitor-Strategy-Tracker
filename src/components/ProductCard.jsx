export default function ProductCard({ product }) {
  return (
    <div className="product-card p-4 border rounded-xl shadow bg-white">
      {/* Product Image */}
      <img
        src={product.image}
        alt={product.name}
        className="w-full h-40 object-cover rounded-md"
      />

      {/* Product Info */}
      <h2 className="text-xl font-semibold mt-3">{product.name}</h2>
      <p className="text-green-600 font-medium mt-1">₹{product.price}</p>

      {/* CTA Button */}
      <button className="mt-4 w-full px-4 py-2 bg-indigo-500 text-white rounded hover:bg-indigo-600">
        Add to Cart
      </button>
    </div>
  );
}
