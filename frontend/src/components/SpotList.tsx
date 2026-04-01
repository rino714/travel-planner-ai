import { api } from "@/api/client";
import type { Spot } from "@/types";

interface Props {
  spots: Spot[];
  onSpotDeleted: (id: number) => void;
}

export default function SpotList({ spots, onSpotDeleted }: Props) {
  const handleDelete = async (id: number) => {
    try {
      await api.deleteSpot(id);
      onSpotDeleted(id);
    } catch (err) {
      alert(err instanceof Error ? err.message : "削除に失敗しました");
    }
  };

  if (spots.length === 0) {
    return <p style={{ color: "#6b7280", textAlign: "center" }}>スポットが登録されていません</p>;
  }

  return (
    <div style={{ marginBottom: 24 }}>
      <h3>📋 登録済みスポット ({spots.length})</h3>
      <ul style={styles.list}>
        {spots.map((spot) => (
          <li key={spot.id} style={styles.item}>
            <div>
              <strong>{spot.name}</strong>
              {spot.address && (
                <span style={styles.address}> — {spot.address}</span>
              )}
              <span style={styles.coords}>
                ({spot.lat.toFixed(4)}, {spot.lng.toFixed(4)})
              </span>
            </div>
            <button onClick={() => handleDelete(spot.id)} style={styles.deleteBtn}>
              ✕
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  list: { listStyle: "none", padding: 0, margin: 0 },
  item: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "10px 12px",
    borderBottom: "1px solid #e5e7eb",
  },
  address: { color: "#6b7280", fontSize: 13 },
  coords: { color: "#9ca3af", fontSize: 12, marginLeft: 8 },
  deleteBtn: {
    background: "none",
    border: "none",
    color: "#dc2626",
    cursor: "pointer",
    fontSize: 16,
    padding: "4px 8px",
  },
};
