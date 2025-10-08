const dummyCompetitors = [
  { product: "Sneakers", competitor: "Amazon", price: 2450 },
  { product: "Sneakers", competitor: "Flipkart", price: 2399 },
];

export default function AdminDashboard() {
  return (
    <div className="min-h-screen bg-gray-50 p-10">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">Admin Dashboard</h1>

      <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-700">Competitor Pricing</h2>
        <table className="w-full border-collapse text-left overflow-hidden rounded-xl">
          <thead className="bg-gradient-to-r from-orange-400 to-amber-500 text-white">
            <tr>
              <th className="p-3">Product</th>
              <th className="p-3">Competitor</th>
              <th className="p-3">Price</th>
            </tr>
          </thead>
          <tbody>
            {dummyCompetitors.map((c, i) => (
              <tr
                key={i}
                className="border-b hover:bg-amber-50 transition"
              >
                <td className="p-3 font-medium">{c.product}</td>
                <td className="p-3">{c.competitor}</td>
                <td className="p-3 text-amber-600 font-semibold">₹{c.price}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
