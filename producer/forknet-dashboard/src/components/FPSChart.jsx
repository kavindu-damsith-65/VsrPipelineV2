import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

export default function FPSChart({ data }) {
  return (
    <div className="bg-slate-800 rounded-xl p-4 shadow-xl">
      <h2 className="text-lg mb-2">Streaming FPS</h2>
      <Line
        data={{
          labels: data.map((_, i) => i),
          datasets: [
            {
              label: "FPS",
              data,
              borderColor: "#38bdf8",
              tension: 0.4,
            },
          ],
        }}
        options={{
          responsive: true,
          scales: { y: { min: 0, max: 60 } },
        }}
      />
    </div>
  );
}
