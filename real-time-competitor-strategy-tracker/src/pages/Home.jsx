import { Link } from "react-router-dom";

export default function Home() {
  return (
    <section className="flex flex-col items-center justify-center text-center p-20 bg-gradient-to-r from-indigo-500 to-purple-600 text-white min-h-screen">
      <h2 className="text-5xl font-bold mb-4">Real-Time Competitor Strategy Tracker</h2>
      <p className="text-lg mb-6">Smarter pricing, seamless shopping, powered by insights.</p>
      <Link
        to="/products"
        className="mt-6 px-6 py-3 bg-white text-black rounded-lg shadow hover:scale-105 transition"
      >
        Explore Products
      </Link>
    </section>
  );
}
