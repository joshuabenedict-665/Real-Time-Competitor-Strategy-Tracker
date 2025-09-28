export default function Home() {
  return (
    <div className="min-h-screen bg-white text-gray-900">
      <header className="p-6 flex justify-between items-center shadow">
        <h1 className="text-3xl font-bold">ShopEase</h1>
        <nav>
          <a href="/products" className="px-4">Products</a>
          <a href="/cart" className="px-4">Cart</a>
        </nav>
      </header>

      <section className="flex flex-col items-center justify-center text-center p-12 bg-gradient-to-r from-blue-500 to-purple-600 text-white">
        <h2 className="text-5xl font-bold mb-4">Shop Smarter, Live Better</h2>
        <p className="text-lg">Minimalistic designs. Premium products. Best prices.</p>
        <a href="/products" className="mt-6 px-6 py-3 bg-white text-black rounded-lg shadow hover:scale-105 transition">Shop Now</a>
      </section>
    </div>
  );
}
