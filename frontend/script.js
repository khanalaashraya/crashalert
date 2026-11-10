const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
const previewArea = document.getElementById("previewArea");
const fileName = document.getElementById("fileName");
const analyzeBtn = document.getElementById("analyzeBtn");
const cameraSelect = document.getElementById("cameraSelect");
const readoutPanel = document.getElementById("readoutPanel");

const resultIcon = document.getElementById("resultIcon");
const accidentStatus = document.getElementById("accidentStatus");
const accidentDetail = document.getElementById("accidentDetail");
const accidentConf = document.getElementById("accidentConf");
const severityValue = document.getElementById("severityValue");
const severityConf = document.getElementById("severityConf");
const locationValue = document.getElementById("locationValue");

const alertBox = document.getElementById("alertBox");
const alertStatus = document.getElementById("alertStatus");
const alertDescription = document.getElementById("alertDescription");

const CAMERA_LOCATIONS = {
  "CAM-01": "KIIT Main Gate",
  "CAM-02": "Campus Road",
  "CAM-03": "Hostel Road",
};

let selectedFile = null;

function formatPct(value) {
  return (value === null || value === undefined || isNaN(Number(value)))
    ? "—"
    : `${(Number(value) * 100).toFixed(1)}%`;
}

cameraSelect.addEventListener("change", () => {
  locationValue.textContent = CAMERA_LOCATIONS[cameraSelect.value];
});

imageInput.addEventListener("change", () => {
  selectedFile = imageInput.files[0];
  if (!selectedFile) return;

  fileName.textContent = selectedFile.name;
  analyzeBtn.disabled = false;
  imagePreview.src = URL.createObjectURL(selectedFile);
  previewArea.classList.add("has-image");
});

function showResult(data) {
  const isAccident = data.accident === true || String(data.accident).toLowerCase() === "true";
  const location = data.location || CAMERA_LOCATIONS[cameraSelect.value] || "Unknown";

  locationValue.textContent = location;
  accidentConf.textContent = formatPct(data.accident_confidence);

  readoutPanel.classList.remove("state-danger", "state-safe");

  if (isAccident) {
    resultIcon.textContent = "!";
    resultIcon.className = "result-icon danger";
    accidentStatus.textContent = "Accident Detected";
    accidentDetail.textContent = "Accident detected by the CrashAlert AI model.";

    severityValue.textContent = data.severity ? `Level ${data.severity}` : "—";
    severityConf.textContent = formatPct(data.severity_confidence);

    alertBox.className = "alert-box danger";
    alertStatus.textContent = data.call_placed
      ? "Phone Call Started"
      : data.alert_generated
        ? "Alert Generated"
        : "Alert Not Generated";
    alertDescription.textContent = data.call_placed
      ? `DialF started a call to the configured contact for ${location}.`
      : data.alert_generated
        ? `A notification was generated for ${location}. ${data.call_reason || "Voice calls may be disabled or not configured."}`
        : "The system did not generate an alert.";

    readoutPanel.classList.add("state-danger");
  } else {
    resultIcon.textContent = "✓";
    resultIcon.className = "result-icon safe";
    accidentStatus.textContent = "No Accident Detected";
    accidentDetail.textContent = "The frame was classified as NonAccident.";

    severityValue.textContent = "Not applicable";
    severityConf.textContent = "—";

    alertBox.className = "alert-box";
    alertStatus.textContent = "No Alert";
    alertDescription.textContent = "No accident was detected, so no emergency alert was generated.";

    readoutPanel.classList.add("state-safe");
  }
}

async function analyze() {
  if (!selectedFile) return;

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";
  accidentStatus.textContent = "Analyzing frame";
  accidentDetail.textContent = "CrashAlert AI pipeline is processing the image.";

  const formData = new FormData();
  formData.append("file", selectedFile);
  formData.append("camera_id", cameraSelect.value);

  try {
    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error(`Backend returned ${response.status}`);

    const data = await response.json();
    showResult(data);

  } catch (error) {
    console.error(error);
    accidentStatus.textContent = "Backend Offline";
    accidentDetail.textContent = "Start the CrashAlert backend (uvicorn) and try again.";
    resultIcon.textContent = "×";
    resultIcon.className = "result-icon";
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze Frame";
  }
}

analyzeBtn.addEventListener("click", analyze);
locationValue.textContent = CAMERA_LOCATIONS[cameraSelect.value];
