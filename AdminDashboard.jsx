import { useEffect, useState } from "react";
import axios from "axios";

export default function AdminDashboard() {
  const [competitorData, setCompetitorData] = useState([]);

  useEffect(() => {
    axios.get("/api/competitors").then(res => setCompetitorData(res.data));
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-6">Admin Dashboard</h1>

      <div className="grid grid-cols-2 gap-6">
        {/* Competitor Pricing Table */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Competitor Pricing</h2>
          <table className="w-full text-left">
            <thead>
              <tr>
                <th>Product</th>
                <th>Competitor</th>
                <th>Price</th>
              </tr>
            </thead>
            <tbody>
              {competitorData.map((c, i) => (
                <tr key={i}>
                  <td>{c.product}</td>
                  <td>{c.competitor}</td>
                  <td>₹{c.price}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pricing Strategy Controls */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Pricing Rules</h2>
          <p className="text-gray-600 mb-2">Set dynamic pricing rules (not visible to customers).</p>
          <button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            Update Pricing Strategy
          </button>
        </div>
      </div>
    </div>
  );
}
