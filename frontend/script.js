const video = document.getElementById('video');
const resultDiv = document.getElementById('result');

let isCameraReady = false;
let isProcessing = false;

// Initialize camera
window.addEventListener('DOMContentLoaded', () => {
  navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(stream => {
      video.srcObject = stream;
      isCameraReady = true;
    })
    .catch(err => {
      resultDiv.textContent = "Camera access denied";
      resultDiv.className = "warning";
    });
});

// ✅ SEND PURE BASE64 (NO HEADER)
function captureFrame() {
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth || 400;
  canvas.height = video.videoHeight || 300;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  // Split and return ONLY base64 part
  return canvas.toDataURL('image/jpeg').split(',')[1];
}

function setProcessing(isProc) {
  isProcessing = isProc;
  const registerBtn = document.getElementById('registerBtn');
  const unlockBtn = document.getElementById('unlockBtn');
  if (registerBtn) registerBtn.disabled = isProc;
  if (unlockBtn) unlockBtn.disabled = isProc;
  if (isProc) {
    if (registerBtn) registerBtn.textContent = "Processing...";
    if (unlockBtn) unlockBtn.textContent = "Processing...";
  } else {
    if (registerBtn) registerBtn.textContent = "Register Face";
    if (unlockBtn) unlockBtn.textContent = "Unlock";
  }
}

// Register
document.getElementById('registerBtn')?.addEventListener('click', async () => {
  if (isProcessing || !isCameraReady) return;

  const name = document.getElementById('nameInput')?.value.trim();
  if (!name) {
    resultDiv.textContent = "Please enter a name";
    resultDiv.className = "warning";
    return;
  }

  setProcessing(true);

  try {
    const frame = captureFrame();
    if (frame.length < 1000) {
      throw new Error("Frame too small");
    }

    const res = await fetch('/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ name, frame }) // PURE base64
    });

    const data = await res.json();
    resultDiv.textContent = res.ok ? data.message : "Registration failed";
    resultDiv.className = res.ok ? "success" : "warning";
    if (res.ok) document.getElementById('nameInput').value = "";
  } catch (e) {
    resultDiv.textContent = "Network error";
    resultDiv.className = "warning";
  } finally {
    setProcessing(false);
  }
});

// Unlock
document.getElementById('unlockBtn')?.addEventListener('click', async () => {
  if (isProcessing || !isCameraReady) return;

  setProcessing(true);

  try {
    const frame = captureFrame();
    if (frame.length < 1000) {
      throw new Error("Frame too small");
    }

    const res = await fetch('/recognize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ frame }) // PURE base64
    });

    const data = await res.json();
    if (res.ok) {
      resultDiv.textContent = data.name === "Unknown" 
        ? "🔒 Unknown Face" 
        : `✅ Welcome, ${data.name}!`;
      resultDiv.className = data.name === "Unknown" ? "warning" : "success";
    } else {
      resultDiv.textContent = "Recognition failed";
      resultDiv.className = "warning";
    }
  } catch (e) {
    resultDiv.textContent = "Network error";
    resultDiv.className = "warning";
  } finally {
    setProcessing(false);
  }
});