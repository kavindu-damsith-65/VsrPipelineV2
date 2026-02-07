export default function VideoInfo({ info }) {
  if (!info) {
    return (
      <div className="bg-slate-800 rounded-xl p-4 text-slate-400">
        Upload a video to view metadata
      </div>
    );
  }

  return (
    <div className="bg-slate-800 rounded-xl p-5 shadow-xl text-sm">
      <h3 className="text-cyan-300 font-semibold mb-3">Video Info</h3>

      <Row label="Resolution" value={info.resolution} />
      <Row label="Native FPS" value={`${info.fps} fps`} />
      <Row label="Duration" value={`${info.duration}s`} />
      <Row label="Bitrate" value={info.bitrate} />
      <Row label="Codec" value={info.codec} />
      <Row label="Total Frames" value={info.frames} />
    </div>
  );
}

function Row({ label, value }) {
  return (
    <div className="flex justify-between border-b border-slate-700 py-1">
      <span className="text-slate-400">{label}</span>
      <span className="text-slate-200 font-medium">{value}</span>
    </div>
  );
}
