import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import AdminNavbar from "../components/AdminNavbar";
import Container from "@mui/material/Container";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import CircularProgress from "@mui/material/CircularProgress";

const API = "http://127.0.0.1:8000";

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [catalog, setCatalog] = useState([]);
  const [scraped, setScraped] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [creating, setCreating] = useState(false);
  const [form, setForm] = useState({ name: "", brand: "", imageUrl: "", basePrice: "" });

  const [scrapeQuery, setScrapeQuery] = useState("");
  const [scrapeMsg, setScrapeMsg] = useState("");
  const [loadingScrape, setLoadingScrape] = useState(false);

  const token = localStorage.getItem("token");
  const headers = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    if (!token) {
      navigate("/login");
      return;
    }
    fetchCatalog();
    fetchScraped();
    fetchPredictions();
  }, []);

  const handleAuthError = (err) => {
    console.error(err);
    if (err.response?.status === 401) {
      localStorage.removeItem("token");
      navigate("/login");
    }
  };

  // Fetch catalog
  const fetchCatalog = () => {
    axios.get(`${API}/products/`, { headers })
      .then(res => {
        const items = res.data.products || [];
        setCatalog(Array.isArray(items) ? items : []);
      })
      .catch(handleAuthError);
  };

  // Fetch scraped competitor pricing - CORRECTED FETCH LOGIC
  const fetchScraped = () => {
    // Calls /admin/scrape/results from the updated routes/scrape.py
    axios.get(`${API}/admin/scrape/results`, { headers })
      .then(res => {
        // Backend returns the array directly (res.data)
        const items = res.data || []; 
        setScraped(Array.isArray(items) ? items : []);
      })
      .catch(handleAuthError);
  };

  // Fetch predictions for your catalog products
  const fetchPredictions = () => {
    axios.get(`${API}/admin/predictions`, { headers })
      .then(res => {
        const items = res.data?.predictions || [];
        setPredictions(Array.isArray(items) ? items : []);
      })
      .catch(handleAuthError);
  };

  const handleScrapeNow = async () => {
    if (!scrapeQuery.trim()) {
      setScrapeMsg("Enter a search keyword");
      return;
    }
    setLoadingScrape(true);
    setScrapeMsg("");

    try {
      // Endpoint is POST /admin/scrape/{query}
      const res = await axios.post(`${API}/admin/scrape/${encodeURIComponent(scrapeQuery)}`, {}, { headers });
      setScrapeMsg(res.data.message || `Scraped ${res.data.count} items`); // Use message from backend
      fetchScraped();
    } catch (err) {
      console.error(err);
      setScrapeMsg(err.response?.data?.detail || "Failed to scrape. Check backend logs.");
    } finally {
      setLoadingScrape(false);
    }
  };

  const handleCreate = (e) => {
    e.preventDefault();
    setCreating(true);

    axios.post(`${API}/admin/products/create`, {
      name: form.name,
      brand: form.brand,
      imageUrl: form.imageUrl,
      basePrice: parseFloat(form.basePrice || 0),
    }, { headers })
      .then(() => {
        setForm({ name: "", brand: "", imageUrl: "", basePrice: "" });
        fetchCatalog();
      })
      .catch(handleAuthError)
      .finally(() => setCreating(false));
  };

  return (
    <div>
      <AdminNavbar />
      <Container sx={{ mt: 4, mb: 6 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>Scrape Competitor Pricing</Typography>
              <TextField
                label="Product name (e.g. Reebok)"
                fullWidth
                value={scrapeQuery}
                onChange={(e) => setScrapeQuery(e.target.value)}
                sx={{ mb: 2 }}
              />
              <Button variant="contained" fullWidth onClick={handleScrapeNow} disabled={loadingScrape}>
                {loadingScrape ? <CircularProgress size={20} color="inherit" /> : "Scrape Now"}
              </Button>
              {scrapeMsg && <Typography sx={{ mt: 2 }}>{scrapeMsg}</Typography>}
            </Paper>

            <Paper sx={{ p: 3, mt: 3 }}>
              <Typography variant="h6" gutterBottom>Create Catalog Product</Typography>
              <Box component="form" onSubmit={handleCreate} sx={{ display: "grid", gap: 1 }}>
                <TextField label="Product name" required value={form.name} onChange={(e) => setForm({...form, name: e.target.value})} />
                <TextField label="Brand" value={form.brand} onChange={(e) => setForm({...form, brand: e.target.value})} />
                <TextField label="Image URL" value={form.imageUrl} onChange={(e) => setForm({...form, imageUrl: e.target.value})} />
                <TextField label="Base Price" value={form.basePrice} onChange={(e) => setForm({...form, basePrice: e.target.value})} />
                <Button type="submit" variant="contained" disabled={creating} sx={{ mt: 1 }}>
                  {creating ? <CircularProgress size={18} color="inherit"/> : "Create Product"}
                </Button>
              </Box>
            </Paper>
          </Grid>

          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2, mb: 3 }}>
              <Typography variant="h6" gutterBottom>Your Catalog</Typography>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Name</TableCell>
                    <TableCell>Brand</TableCell>
                    <TableCell>Image</TableCell>
                    <TableCell>Base Price</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {catalog.map(p => (
                    <TableRow key={p._id}>
                      <TableCell>{p.name}</TableCell>
                      <TableCell>{p.brand}</TableCell>
                      <TableCell>{p.imageUrl ? <img src={p.imageUrl} alt="" style={{ width: 60 }} /> : "-"}</TableCell>
                      <TableCell>₹{p.basePrice}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Paper>

            <Paper sx={{ p: 2, mb: 3 }}>
              <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <Typography variant="h6">Competitor Scraped Prices</Typography>
                <Button size="small" onClick={fetchScraped}>Reload</Button>
              </Box>
              <Table size="small">
                <TableHead>
                  <TableRow><TableCell>Product</TableCell><TableCell>Price</TableCell><TableCell>Platform</TableCell></TableRow>
                </TableHead>
                <TableBody>
                  {scraped.map((s, i) => (
                    <TableRow key={s._id || i}> {/* Use _id if available */}
                      {/* Using name, basePrice, and source/competitor as returned by routes/admin.py or routes/scrape.py */}
                      <TableCell>{s.name || "-"}</TableCell> 
                      <TableCell>₹{s.basePrice ?? s.price ?? "-"}</TableCell> 
                      <TableCell>{s.source || s.competitor || "—"}</TableCell> 
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Paper>

            <Paper sx={{ p: 2 }}>
              <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <Typography variant="h6">Predicted Prices for Your Products</Typography>
                <Button size="small" onClick={fetchPredictions}>Reload</Button>
              </Box>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Product</TableCell>
                    <TableCell>Base Price</TableCell>
                    <TableCell>Predicted Price</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {predictions.map((pr, i) => (
                    <TableRow key={pr.product_id || i}>
                      <TableCell>{pr.product_name}</TableCell>
                      <TableCell>₹{pr.base_price ?? "—"}</TableCell>
                      <TableCell>
                        <Box sx={{ 
                           fontWeight: 700, 
                           color: pr.predicted_price > 0 && pr.predicted_price > pr.base_price ? 'lightgreen' : (pr.predicted_price > 0 && pr.predicted_price < pr.base_price ? 'pink' : 'inherit')
                        }}>
                           {pr.predicted_price > 0 ? `₹${pr.predicted_price}` : "N/A"} 
                        </Box>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </div>
  );
}