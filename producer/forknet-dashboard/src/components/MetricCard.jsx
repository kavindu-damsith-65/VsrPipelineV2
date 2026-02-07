export default function MetricCard({ title, value }) {
  return (
    <div className="bg-slate-800 rounded-xl p-4 text-center shadow-xl">
      <p className="text-sm text-slate-400">{title}</p>
      <p className="text-2xl font-bold text-cyan-400">{value}</p>
    </div>
  );
}
