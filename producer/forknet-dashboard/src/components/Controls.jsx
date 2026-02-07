import axios from "axios";

const API = "http://localhost:5000";

export default function Controls({ onUpload }) {
  const upload = async (e) => {
    const form = new FormData();
    form.append("video", e.target.files[0]);
    await axios.post(`${API}/upload`, form);
    onUpload();
  };

  return (
    <div className="bg-slate-800 rounded-xl p-5 shadow-xl flex flex-wrap gap-4 items-center">
      <label className="cursor-pointer bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg">
        📁 Upload Video
        <input type="file" className="hidden" onChange={upload} />
      </label>

      <button
        onClick={() => axios.get(`${API}/start`)}
        className="control-btn bg-green-600"
      >
        ▶ Start (GPU)
      </button>

      <button
        onClick={() => axios.get(`${API}/pause`)}
        className="control-btn bg-yellow-500"
      >
        ⏸ Pause
      </button>

      <button
        onClick={() => axios.get(`${API}/stop`)}
        className="control-btn bg-red-600"
      >
        ⏹ Stop
      </button>
    </div>
  );
}
