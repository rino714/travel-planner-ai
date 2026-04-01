import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "@/api/client";
import type { Spot } from "@/types";
import SpotInput from "@/components/SpotInput";
import SpotList from "@/components/SpotList";

export default function HomePage() {
  const navigate = useNavigate();
  const [spots, setSpots] = useState<Spot[]>([]);
  const [startDate, setStartDate] = useState("");
  const [days, setDays] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api.listSpots().then(setSpots).catch(console.error);
  }, []);

  const handleSpotAdded = (spot: Spot) => {
    setSpots((prev) => [spot, ...prev]);
  };

  const handleSpotDeleted = (id: number) => {
    setSpots((prev) => prev.filter((s) => s.id !== id));
  };

  const handleCreatePlan = async () => {
    if (spots.length === 0 || !startDate) return;

    setLoading(true);
    setError("");

    try {
      const trip = await api.createTrip({
        spot_ids: spots.map((s) => s.id),
        start_date: startDate,
        days,
      });
      navigate(`/plan/${trip.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "プラン生成に失敗しました");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <SpotInput onSpotAdded={handleSpotAdded} />
      <SpotList spots={spots} onSpotDeleted={handleSpotDeleted} />

      <div style={styles.planSection}>
        <h3>🗓️ プランを作成</h3>
        <div style={styles.row}>
          <label style={styles.label}>
            出発日
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              style={styles.input}
              required
            />
          </label>
          <label style={styles.label}>
            日数
            <select
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              style={styles.input}
            >
              {[1, 2, 3, 4, 5, 6, 7].map((d) => (
                <option key={d} value={d}>
                  {d}日
                </option>
              ))}
            </select>
          </label>
        </div>

        {error && <p style={styles.error}>{error}</p>}

        <button
          onClick={handleCreatePlan}
          disabled={loading || spots.length === 0 || !startDate}
          style={{
            ...styles.btn,
            opacity: spots.length === 0 || !startDate ? 0.5 : 1,
          }}
        >
          {loading ? "生成中..." : `プランを作成（${spots.length}スポット）`}
        </button>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  planSection: {
    border: "1px solid #ddd",
    borderRadius: 8,
    padding: 20,
    backgroundColor: "#f0f9ff",
  },
  row: { display: "flex", gap: 16, marginBottom: 16, flexWrap: "wrap" },
  label: { display: "flex", flexDirection: "column", gap: 4, fontSize: 14 },
  input: { padding: 8, borderRadius: 4, border: "1px solid #ccc" },
  btn: {
    padding: "12px 32px",
    backgroundColor: "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: 6,
    cursor: "pointer",
    fontSize: 16,
    fontWeight: "bold",
  },
  error: { color: "#dc2626", fontSize: 13, marginBottom: 8 },
};
