export default function VideoDetails({ metrics }) {
  return (
    <div className="bg-slate-800 rounded-xl p-5 shadow-xl h-full">
      <h2 className="text-lg font-semibold mb-4 text-cyan-300">
        Stream Details
      </h2>

      <div className="space-y-3 text-sm">
        <Detail label="Status" value={metrics.status} highlight />
        <Detail label="Streaming FPS" value={metrics.fps} />
        <Detail label="Frames Sent" value={metrics.frames_sent} />
        <Detail label="Resolution" value="240p (Input)" />
        <Detail label="Codec" value="MJPEG" />
        <Detail label="Mode" value="Virtual Live Stream" />
      </div>
    </div>
  );
}

function Detail({ label, value, highlight }) {
  return (
    <div className="flex justify-between border-b border-slate-700 pb-2">
      <span className="text-slate-400">{label}</span>
      <span
        className={`font-semibold ${
          highlight ? "text-green-400" : "text-slate-200"
        }`}
      >
        {value ?? "--"}
      </span>
    </div>
  );
}
