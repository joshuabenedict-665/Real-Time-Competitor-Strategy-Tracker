import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext";

export default function Navbar() {
  const { cartItems } = useCart();

  return (
    <header className="sticky top-0 z-50 bg-gradient-to-r from-amber-400 via-orange-500 to-red-500 text-white shadow-lg">
      <div className="container mx-auto flex justify-between items-center px-6 py-4">
        <h1 className="text-2xl font-extrabold tracking-wide drop-shadow-md">
          ShopSmart
        </h1>

        <nav className="flex items-center space-x-8 font-semibold">
          <Link to="/" className="hover:text-gray-900 transition-colors">Home</Link>
          <Link to="/products" className="hover:text-gray-900 transition-colors">Products</Link>
          <Link to="/cart" className="relative hover:text-gray-900 transition-colors">
            Cart
            {cartItems.length > 0 && (
              <span className="absolute -top-2 -right-3 bg-black text-white rounded-full w-5 h-5 flex items-center justify-center text-xs font-bold">
                {cartItems.reduce((a, c) => a + c.quantity, 0)}
              </span>
            )}
          </Link>
          <Link
            to="/admin/login"
            className="bg-black text-white px-4 py-1.5 rounded-lg hover:bg-gray-800 transition"
          >
            Admin
          </Link>
        </nav>
      </div>
    </header>
  );
}
