const dummyCompetitors = [
  { product: "Sneakers", competitor: "Amazon", price: 2450 },
  { product: "Sneakers", competitor: "Flipkart", price: 2399 },
];

export default function AdminDashboard() {
  return (
    <div className="p-8 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Admin Dashboard</h1>
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Competitor Pricing</h2>
        <table className="w-full text-left border-collapse">
          <thead>
            <tr>
              <th className="border-b p-2">Product</th>
              <th className="border-b p-2">Competitor</th>
              <th className="border-b p-2">Price</th>
            </tr>
          </thead>
          <tbody>
            {dummyCompetitors.map((c, i) => (
              <tr key={i}>
                <td className="p-2">{c.product}</td>
                <td className="p-2">{c.competitor}</td>
                <td className="p-2">₹{c.price}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
