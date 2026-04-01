import type { ScheduleItem } from "@/types";

interface Props {
  items: ScheduleItem[];
}

const ICONS: Record<string, string> = {
  spot: "📍",
  move: "🚗",
  accommodation: "🏨",
};

export default function Timeline({ items }: Props) {
  return (
    <div style={styles.container}>
      {items.map((item, idx) => (
        <div key={idx} style={styles.row}>
          <div style={styles.time}>{item.time}</div>
          <div style={styles.line}>
            <div style={styles.dot(item.type)} />
            {idx < items.length - 1 && <div style={styles.connector} />}
          </div>
          <div style={styles.content}>
            <span style={styles.icon}>{ICONS[item.type] ?? "📌"}</span>
            <div>
              <div style={styles.name}>{item.name}</div>
              {item.duration_min != null && (
                <div style={styles.duration}>{item.duration_min}分</div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

const DOT_COLORS: Record<string, string> = {
  spot: "#2563eb",
  move: "#f59e0b",
  accommodation: "#10b981",
};

const styles = {
  container: { padding: "16px" } as React.CSSProperties,
  row: {
    display: "flex",
    alignItems: "flex-start",
    position: "relative" as const,
    minHeight: 48,
  } as React.CSSProperties,
  time: {
    width: 50,
    fontSize: 13,
    color: "#6b7280",
    paddingTop: 2,
    textAlign: "right" as const,
    marginRight: 12,
  } as React.CSSProperties,
  line: {
    display: "flex",
    flexDirection: "column" as const,
    alignItems: "center",
    width: 20,
    marginRight: 12,
  } as React.CSSProperties,
  dot: (type: string): React.CSSProperties => ({
    width: 12,
    height: 12,
    borderRadius: "50%",
    backgroundColor: DOT_COLORS[type] ?? "#9ca3af",
    flexShrink: 0,
    marginTop: 4,
  }),
  connector: {
    width: 2,
    flex: 1,
    backgroundColor: "#d1d5db",
    minHeight: 24,
  } as React.CSSProperties,
  content: {
    display: "flex",
    gap: 8,
    alignItems: "flex-start",
    flex: 1,
    paddingBottom: 12,
  } as React.CSSProperties,
  icon: { fontSize: 18 } as React.CSSProperties,
  name: { fontWeight: 500, fontSize: 14 } as React.CSSProperties,
  duration: { fontSize: 12, color: "#6b7280" } as React.CSSProperties,
};
