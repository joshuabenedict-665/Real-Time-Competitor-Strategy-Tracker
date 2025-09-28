export default function Navbar() {
  return (
    <header className="p-6 flex justify-between items-center shadow bg-white">
      <h1 className="text-2xl font-bold text-indigo-600">
        Real-Time Competitor Strategy Tracker
      </h1>
      <nav>
        <a href="/" className="px-4">Home</a>
        <a href="/products" className="px-4">Products</a>
        <a href="/cart" className="px-4">Cart</a>
      </nav>
    </header>
  );
}