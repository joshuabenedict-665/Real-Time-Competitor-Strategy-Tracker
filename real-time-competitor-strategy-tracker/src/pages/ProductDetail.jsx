import { useParams } from "react-router-dom";
import { useCart } from "../context/CartContext";

const dummyProducts = [
  { id: 1, name: "Sneakers", price: 2500, desc: "Comfortable running sneakers.", image: "/sneakers.jpg" },
  { id: 2, name: "Headphones", price: 4999, desc: "Noise-cancelling wireless headphones.", image: "/headphones.jpg" },
  { id: 3, name: "Smartwatch", price: 6999, desc: "Track your fitness and notifications.", image: "/smartwatch.jpg" },
];

export default function ProductDetail() {
  const { id } = useParams();
  const product = dummyProducts.find(p => p.id.toString() === id);
  const { addToCart } = useCart();

  if (!product) return <p className="p-8">Product not found.</p>;

  return (
    <div className="p-8 flex flex-col md:flex-row gap-8">
      <img src={product.image} alt={product.name} className="w-full md:w-1/3 rounded-lg" />
      <div>
        <h1 className="text-3xl font-bold">{product.name}</h1>
        <p className="text-green-600 text-xl my-4">₹{product.price}</p>
        <p className="text-gray-700 mb-4">{product.desc}</p>
        <button
          onClick={() => addToCart(product)}
          className="px-6 py-3 bg-indigo-500 text-white rounded hover:bg-indigo-600"
        >
          Add to Cart
        </button>
      </div>
    </div>
  );
}