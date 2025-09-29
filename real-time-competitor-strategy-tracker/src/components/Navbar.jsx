import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext";

export default function Navbar() {
  const { cartItems } = useCart();

  return (
    <header className="p-6 flex justify-between items-center shadow bg-white sticky top-0 z-50">
      <h1 className="text-2xl font-bold text-indigo-600">
        Real-Time Competitor Strategy Tracker
      </h1>
      <nav className="flex items-center space-x-4">
        <Link to="/" className="hover:text-indigo-600">Home</Link>
        <Link to="/products" className="hover:text-indigo-600">Products</Link>
        <Link to="/cart" className="relative hover:text-indigo-600">
          Cart
          {cartItems.length > 0 && (
            <span className="absolute -top-2 -right-3 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs">
              {cartItems.reduce((a, c) => a + c.quantity, 0)}
            </span>
          )}
        </Link>
      </nav>
    </header>
  );
}
