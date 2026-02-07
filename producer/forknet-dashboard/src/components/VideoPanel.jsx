export default function VideoPanel() {
  return (
    <div className="bg-slate-800 rounded-xl p-4 shadow-xl">
      <h2 className="text-lg font-semibold mb-2">Live Preview</h2>
      <img
        src="http://localhost:5000/stream"
        className="rounded-lg border border-slate-700 w-full"
      />
    </div>
  );
}
