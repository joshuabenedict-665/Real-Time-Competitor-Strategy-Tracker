import { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function AdminDashboard() {
  const [data, setData] = useState(null);
  const [prices, setPrices] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("token");
        const res = await fetch("http://localhost:8000/admin/dashboard", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) {
          const j = await res.json().catch(()=>({detail:""}));
          throw new Error(j.detail || j.error || "Unauthorized or server error");
        }
        const json = await res.json();
        setData(json);
        const merged = (json.scraped_prices || []).map((item) => ({
          name: item.get?.("name") || item.name,
          scraped_price: item.get?.("price") || item.price,
          predicted_price: (json.predicted_prices || []).find(p => p.name === item.name)?.predicted_price ?? null
        }));
        // If the mapping above fails due to optional chaining older env, fallback:
        const safeMerged = (json.scraped_prices || []).map(item => ({
          name: item.name,
          scraped_price: item.price,
          predicted_price: (json.predicted_prices || []).find(p => p.name === item.name)?.predicted_price ?? null
        }));
        setPrices(safeMerged);
      } catch (err) {
        setError("❌ " + err.message);
      }
    };
    fetchData();
  }, []);

  if (error) return <div className="p-6 text-red-600">{error}</div>;
  if (!data) return <div className="p-6">Loading dashboard...</div>;

  const chartData = {
    labels: prices.map((p) => p.name),
    datasets: [
      {
        label: "Scraped Price",
        data: prices.map((p) => p.scraped_price || 0),
      },
      {
        label: "Predicted Price",
        data: prices.map((p) => p.predicted_price || 0),
      },
    ],
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl mb-4">Admin Dashboard</h1>
      <p className="mb-2"><strong>Scraper Status:</strong> {data.scraper_status}</p>
      <p className="mb-4"><strong>Monitored:</strong> {prices.length}</p>

      {prices.length > 0 ? (
        <>
          <div className="mb-6" style={{ maxWidth: 800 }}>
            <Bar data={chartData} />
          </div>

          <table className="w-full border-collapse" style={{ border: "1px solid #ddd" }}>
            <thead>
              <tr>
                <th className="p-2">Name</th>
                <th className="p-2">Scraped Price</th>
                <th className="p-2">Predicted Price</th>
              </tr>
            </thead>
            <tbody>
              {prices.map((p, idx) => (
                <tr key={idx} className="border-t">
                  <td className="p-2">{p.name}</td>
                  <td className="p-2">₹{p.scraped_price ?? "N/A"}</td>
                  <td className="p-2">₹{p.predicted_price ?? "N/A"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      ) : (
        <div>No data</div>
      )}
    </div>
  );
}
