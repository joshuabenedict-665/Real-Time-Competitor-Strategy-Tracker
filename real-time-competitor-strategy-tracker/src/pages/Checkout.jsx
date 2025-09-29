import { useCart } from "../context/CartContext";

export default function Checkout() {
  const { cartItems } = useCart();

  if (cartItems.length === 0) {
    return (
      <div className="p-8">
        <h1 className="text-3xl font-bold mb-6">Checkout</h1>
        <p>Your cart is empty.</p>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-lg mx-auto">
      <h1 className="text-3xl font-bold mb-6">Checkout</h1>
      <form className="bg-white p-6 rounded-lg shadow space-y-4">
        <input type="text" placeholder="Name" className="w-full p-3 border rounded" />
        <input type="email" placeholder="Email" className="w-full p-3 border rounded" />
        <input type="text" placeholder="Address" className="w-full p-3 border rounded" />
        <button type="submit" className="w-full bg-indigo-500 text-white p-3 rounded hover:bg-indigo-600">
          Place Order
        </button>
      </form>
      <div className="mt-6">
        <h2 className="text-xl font-semibold mb-2">Order Summary</h2>
        {cartItems.map(item => (
          <div key={item.id} className="flex justify-between">
            <span>{item.name} x {item.quantity}</span>
            <span>₹{item.price * item.quantity}</span>
          </div>
        ))}
        <div className="flex justify-between font-bold mt-2">
          <span>Total</span>
          <span>₹{cartItems.reduce((a, c) => a + c.price * c.quantity, 0)}</span>
        </div>
      </div>
    </div>
  );
}
