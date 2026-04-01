import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "@/api/client";
import type { Trip } from "@/types";
import PlanResult from "@/components/PlanResult";

export default function PlanPage() {
  const { tripId } = useParams<{ tripId: string }>();
  const [trip, setTrip] = useState<Trip | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!tripId) return;
    api
      .getTrip(Number(tripId))
      .then(setTrip)
      .catch((err) =>
        setError(err instanceof Error ? err.message : "取得に失敗しました")
      );
  }, [tripId]);

  if (error) {
    return (
      <div style={{ textAlign: "center" }}>
        <p style={{ color: "#dc2626" }}>{error}</p>
        <Link to="/">← ホームに戻る</Link>
      </div>
    );
  }

  if (!trip) {
    return <p style={{ textAlign: "center" }}>読み込み中...</p>;
  }

  return (
    <div>
      <Link to="/" style={styles.backLink}>
        ← スポット一覧に戻る
      </Link>

      <div style={styles.header}>
        <h2>旅行プラン</h2>
        <p style={styles.meta}>
          {trip.start_date} から {trip.days}日間
        </p>
      </div>

      <PlanResult schedule={trip.schedule} />
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  backLink: {
    display: "inline-block",
    marginBottom: 16,
    color: "#2563eb",
    textDecoration: "none",
  },
  header: { marginBottom: 24 },
  meta: { color: "#6b7280", fontSize: 14, marginTop: 4 },
};
