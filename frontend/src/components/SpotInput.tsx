import { useState } from "react";
import { api } from "@/api/client";
import type { Spot } from "@/types";

interface Props {
  onSpotAdded: (spot: Spot) => void;
}

export default function SpotInput({ onSpotAdded }: Props) {
  const [name, setName] = useState("");
  const [address, setAddress] = useState("");
  const [lat, setLat] = useState("");
  const [lng, setLng] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleGeocode = async () => {
    if (!name.trim()) return;
    setLoading(true);
    setError("");

    try {
      const query = address || name;
      const res = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`,
        { headers: { "User-Agent": "TravelPlannerAI/0.1" } }
      );
      const data = await res.json();
      if (data.length > 0) {
        setLat(data[0].lat);
        setLng(data[0].lon);
      } else {
        setError("住所から座標を取得できませんでした。手動で入力してください。");
      }
    } catch {
      setError("ジオコーディングに失敗しました。");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !lat || !lng) return;

    setLoading(true);
    setError("");

    try {
      const spot = await api.createSpot({
        name: name.trim(),
        address: address || undefined,
        lat: parseFloat(lat),
        lng: parseFloat(lng),
      });
      onSpotAdded(spot);
      setName("");
      setAddress("");
      setLat("");
      setLng("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "登録に失敗しました");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <h3>📍 スポットを追加</h3>

      <div style={styles.row}>
        <input
          type="text"
          placeholder="スポット名（例：東京タワー）"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={styles.input}
          required
        />
        <input
          type="text"
          placeholder="住所（任意）"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          style={styles.input}
        />
      </div>

      <div style={styles.row}>
        <input
          type="number"
          step="any"
          placeholder="緯度"
          value={lat}
          onChange={(e) => setLat(e.target.value)}
          style={styles.inputSmall}
          required
        />
        <input
          type="number"
          step="any"
          placeholder="経度"
          value={lng}
          onChange={(e) => setLng(e.target.value)}
          style={styles.inputSmall}
          required
        />
        <button
          type="button"
          onClick={handleGeocode}
          disabled={loading || !name.trim()}
          style={styles.btnSecondary}
        >
          座標を自動取得
        </button>
      </div>

      {error && <p style={styles.error}>{error}</p>}

      <button type="submit" disabled={loading} style={styles.btn}>
        {loading ? "追加中..." : "スポットを追加"}
      </button>
    </form>
  );
}

const styles: Record<string, React.CSSProperties> = {
  form: {
    border: "1px solid #ddd",
    borderRadius: 8,
    padding: 20,
    marginBottom: 24,
    backgroundColor: "#fafafa",
  },
  row: { display: "flex", gap: 8, marginBottom: 12, flexWrap: "wrap" },
  input: { flex: 1, padding: 8, borderRadius: 4, border: "1px solid #ccc", minWidth: 180 },
  inputSmall: { width: 120, padding: 8, borderRadius: 4, border: "1px solid #ccc" },
  btn: {
    padding: "10px 24px",
    backgroundColor: "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: 6,
    cursor: "pointer",
    fontSize: 14,
  },
  btnSecondary: {
    padding: "8px 16px",
    backgroundColor: "#6b7280",
    color: "#fff",
    border: "none",
    borderRadius: 6,
    cursor: "pointer",
    fontSize: 13,
  },
  error: { color: "#dc2626", fontSize: 13, marginBottom: 8 },
};
