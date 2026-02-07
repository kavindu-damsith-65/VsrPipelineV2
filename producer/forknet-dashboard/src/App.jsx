import { useEffect, useState } from "react";
import axios from "axios";

import Controls from "./components/Controls";
import VideoPanel from "./components/VideoPanel";
import VideoInfo from "./components/VideoInfo";

const API = "http://localhost:5000";

export default function App() {
  const [metrics, setMetrics] = useState({});
  const [videoInfo, setVideoInfo] = useState(null);

  // Poll live metrics
  useEffect(() => {
    const id = setInterval(async () => {
      const res = await axios.get(`${API}/metrics`);
      setMetrics(res.data);
    }, 500);
    return () => clearInterval(id);
  }, []);

  const handleUpload = async () => {
    const res = await axios.get(`${API}/video_info`);
    if (res.data.loaded !== false) {
      setVideoInfo(res.data);
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-cyan-400">
        ForkNet – Live Producer Studio
      </h1>

      <Controls onUpload={handleUpload} />

      {/* 70 / 30 layout */}
      <div className="grid grid-cols-10 gap-6">
        <div className="col-span-7 space-y-4">
          <VideoPanel />
          <VideoInfo info={videoInfo} />
        </div>

        <div className="col-span-3 bg-slate-800 rounded-xl p-5 shadow-xl text-sm">
          <h3 className="text-cyan-300 font-semibold mb-3">
            Live Stream Status
          </h3>

          <Row label="Status" value={metrics.status} highlight />
          <Row label="Streaming FPS" value={metrics.fps} />
          <Row label="Frames Sent" value={metrics.frames_sent} />
          <Row label="Pipeline" value="NVDEC → NVENC (GPU)" />
        </div>
      </div>
    </div>
  );
}

function Row({ label, value, highlight }) {
  return (
    <div className="flex justify-between border-b border-slate-700 py-2">
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
