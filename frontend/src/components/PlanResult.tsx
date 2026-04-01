import type { DaySchedule } from "@/types";
import Timeline from "./Timeline";

interface Props {
  schedule: DaySchedule[];
}

export default function PlanResult({ schedule }: Props) {
  return (
    <div>
      {schedule.map((day) => (
        <div key={day.day} style={styles.dayBlock}>
          <h3 style={styles.dayHeader}>
            Day {day.day} — {day.date}
          </h3>
          <Timeline items={day.items} />
        </div>
      ))}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  dayBlock: {
    marginBottom: 32,
    border: "1px solid #e5e7eb",
    borderRadius: 8,
    overflow: "hidden",
  },
  dayHeader: {
    margin: 0,
    padding: "12px 16px",
    backgroundColor: "#2563eb",
    color: "#fff",
    fontSize: 16,
  },
};
