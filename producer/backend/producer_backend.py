import cv2
import time
import json
import signal
import subprocess
from flask import Flask, Response, request, jsonify
from flask_cors import CORS

# ==========================================================
# APP
# ==========================================================
app = Flask(__name__)
CORS(app)

# ==========================================================
# GLOBAL STATE
# ==========================================================
INPUT_VIDEO = "input.mp4"
GPU_STREAM_URL = "udp://127.0.0.1:5001"

cap = None
ffmpeg_proc = None

video_info = None
video_fps = None
frame_interval = None

streaming = False
paused = False

metrics = {
    "fps": 0.0,
    "frames_sent": 0,
    "status": "STOPPED"
}

# ==========================================================
# METADATA EXTRACTION (SOURCE OF TRUTH)
# ==========================================================
def extract_metadata(path):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries",
        "stream=width,height,r_frame_rate,codec_name,nb_frames",
        "-show_entries",
        "format=duration,bit_rate",
        "-of", "json",
        path
    ]

    meta = json.loads(subprocess.check_output(cmd))

    stream = meta["streams"][0]
    fmt = meta["format"]

    fps = eval(stream["r_frame_rate"])

    return {
        "width": stream["width"],
        "height": stream["height"],
        "resolution": f'{stream["width"]} x {stream["height"]}',
        "fps": round(fps, 2),
        "codec": stream["codec_name"],
        "bitrate": f'{int(fmt["bit_rate"]) // 1000} kbps',
        "duration": round(float(fmt["duration"]), 2),
        "frames": int(stream.get("nb_frames", 0)),
    }

# ==========================================================
# GPU STREAM (NVENC)
# ==========================================================
def start_gpu_stream():
    global ffmpeg_proc

    if ffmpeg_proc is not None:
        return

    cmd = [
        "ffmpeg",
        "-re",                         # native timing
        "-hwaccel", "cuda",            # GPU decode
        "-i", INPUT_VIDEO,
        "-c:v", "h264_nvenc",          # GPU encode (RTX 2050)
        "-preset", "p1",
        "-tune", "ll",
        "-rc", "cbr",
        "-b:v", "2M",
        "-f", "mpegts",
        GPU_STREAM_URL
    ]

    ffmpeg_proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def stop_gpu_stream():
    global ffmpeg_proc
    if ffmpeg_proc:
        ffmpeg_proc.send_signal(signal.SIGINT)
        ffmpeg_proc = None

# ==========================================================
# MJPEG PREVIEW STREAM (NATIVE FPS)
# ==========================================================
def mjpeg_generator():
    global metrics

    next_frame_time = time.time()

    while True:
        if not streaming or paused or cap is None:
            time.sleep(0.05)
            continue

        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            next_frame_time = time.time()
            continue

        # enforce native FPS
        now = time.time()
        sleep_time = next_frame_time - now
        if sleep_time > 0:
            time.sleep(sleep_time)

        next_frame_time += frame_interval

        metrics["fps"] = video_fps
        metrics["frames_sent"] += 1

        _, buffer = cv2.imencode(
            ".jpg",
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, 60]
        )

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            buffer.tobytes() +
            b"\r\n"
        )

# ==========================================================
# ROUTES — UI CONTROLS EVERYTHING
# ==========================================================
@app.route("/upload", methods=["POST"])
def upload():
    global cap, video_info, video_fps, frame_interval

    file = request.files["video"]
    file.save(INPUT_VIDEO)

    # extract metadata FIRST
    video_info = extract_metadata(INPUT_VIDEO)

    # open video
    cap = cv2.VideoCapture(INPUT_VIDEO)

    # native FPS from video
    video_fps = video_info["fps"]
    frame_interval = 1.0 / video_fps

    metrics["frames_sent"] = 0
    metrics["fps"] = video_fps
    metrics["status"] = "READY"

    return jsonify({
        "status": "uploaded",
        "video_info": video_info
    })

@app.route("/start")
def start():
    global streaming, paused

    if cap is None:
        return jsonify({"error": "No video uploaded"}), 400

    streaming = True
    paused = False
    metrics["status"] = "LIVE"

    start_gpu_stream()
    return jsonify({"status": "started"})

@app.route("/pause")
def pause():
    global paused
    paused = True
    metrics["status"] = "PAUSED"
    return jsonify({"status": "paused"})

@app.route("/stop")
def stop():
    global streaming, paused

    streaming = False
    paused = False
    metrics["status"] = "STOPPED"

    stop_gpu_stream()
    return jsonify({"status": "stopped"})

@app.route("/stream")
def stream():
    return Response(
        mjpeg_generator(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/metrics")
def get_metrics():
    return jsonify(metrics)

@app.route("/video_info")
def get_video_info():
    return jsonify(video_info if video_info else {"loaded": False})

# ==========================================================
# RUN
# ==========================================================
if __name__ == "__main__":
    print("Backend running at http://localhost:5000")
    print("GPU stream available at udp://127.0.0.1:5001")
    app.run(host="0.0.0.0", port=5000, threaded=True)
