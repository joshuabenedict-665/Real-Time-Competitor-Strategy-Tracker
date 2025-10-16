import { useEffect, useState } from "react";

export default function AdminDashboard() {
  const [competitors, setCompetitors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch live product data from FastAPI
    fetch("http://127.0.0.1:8000/products")
      .then((res) => res.json())
      .then((data) => {
        // Map backend products to competitor-style data for table
        const formatted = data.map((p) => ({
          product: p.name,
          competitor: p.category, // Using category as placeholder for competitor
          price: p.current_price,
        }));
        setCompetitors(formatted);
      })
      .catch((err) => console.error("Error fetching data:", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="p-10 text-center text-gray-500 text-lg">
        Loading competitor data...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-10">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">Admin Dashboard</h1>

      <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-700">
          Competitor Pricing
        </h2>

        {competitors.length === 0 ? (
          <p className="text-center text-gray-500 py-10">
            No competitor data available.
          </p>
        ) : (
          <table className="w-full border-collapse text-left overflow-hidden rounded-xl">
            <thead className="bg-gradient-to-r from-orange-400 to-amber-500 text-white">
              <tr>
                <th className="p-3">Product</th>
                <th className="p-3">Competitor</th>
                <th className="p-3">Price</th>
              </tr>
            </thead>
            <tbody>
              {competitors.map((c, i) => (
                <tr
                  key={i}
                  className="border-b hover:bg-amber-50 transition"
                >
                  <td className="p-3 font-medium">{c.product}</td>
                  <td className="p-3">{c.competitor}</td>
                  <td className="p-3 text-amber-600 font-semibold">
                    ₹{c.price}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
