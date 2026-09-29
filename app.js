const video = document.querySelector('#video');
const canvas = document.querySelector('#motionCanvas');
const ctx = canvas.getContext('2d', { willReadFrequently: true });
const startButton = document.querySelector('#startButton');
const stopButton = document.querySelector('#stopButton');
const autoFollow = document.querySelector('#autoFollow');
const centerBall = document.querySelector('#centerBall');
const stage = document.querySelector('#stage');
const hint = document.querySelector('#hint');
const status = document.querySelector('#status');
const objectCount = document.querySelector('#objectCount');

let stream;
let previousFrame;
let animationId;
let targets = [];
let selectedTarget = null;

startButton.addEventListener('click', startCamera);
stopButton.addEventListener('click', stopCamera);
canvas.addEventListener('click', (event) => {
  const rect = canvas.getBoundingClientRect();
  const x = (event.clientX - rect.left) / rect.width;
  const y = (event.clientY - rect.top) / rect.height;
  selectedTarget = targets.find((target) => Math.hypot(target.x - x, target.y - y) < .1) || null;
  centerBall.classList.toggle('following', Boolean(selectedTarget));
  if (selectedTarget) status.textContent = 'Objeto selecionado';
});

async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' }, audio: false });
    video.srcObject = stream;
    await video.play();
    canvas.width = 320;
    canvas.height = 180;
    previousFrame = null;
    startButton.disabled = true;
    stopButton.disabled = false;
    hint.hidden = true;
    status.textContent = 'Detectando movimento...';
    detectMotion();
  } catch (error) {
    status.textContent = error.name === 'NotAllowedError' ? 'Permissão da câmera negada' : 'Não foi possível iniciar a câmera';
  }
}

function stopCamera() {
  cancelAnimationFrame(animationId);
  stream?.getTracks().forEach((track) => track.stop());
  video.srcObject = null;
  previousFrame = null;
  targets = [];
  selectedTarget = null;
  centerBall.style.left = '50%';
  centerBall.style.top = '50%';
  centerBall.classList.remove('following');
  objectCount.textContent = 'Objetos detectados: 0';
  hint.hidden = false;
  startButton.disabled = false;
  stopButton.disabled = true;
  status.textContent = 'Câmera parada';
}

function detectMotion() {
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const current = ctx.getImageData(0, 0, canvas.width, canvas.height);
  if (!previousFrame) { previousFrame = current; animationId = requestAnimationFrame(detectMotion); return; }

  const mask = new Uint8Array(canvas.width * canvas.height);
  for (let y = 0; y < canvas.height; y += 2) {
    for (let x = 0; x < canvas.width; x += 2) {
      const i = (y * canvas.width + x) * 4;
      const difference = Math.abs(current.data[i] - previousFrame.data[i]) + Math.abs(current.data[i + 1] - previousFrame.data[i + 1]) + Math.abs(current.data[i + 2] - previousFrame.data[i + 2]);
      if (difference > 85) mask[y * canvas.width + x] = 1;
    }
  }
  targets = findClusters(mask);
  objectCount.textContent = `Objetos detectados: ${targets.length}`;
  if (selectedTarget && autoFollow.checked) {
    const nearest = targets.sort((a, b) => Math.hypot(a.x - selectedTarget.x, a.y - selectedTarget.y) - Math.hypot(b.x - selectedTarget.x, b.y - selectedTarget.y))[0];
    if (nearest) { selectedTarget = nearest; moveVirtualCursor(nearest.x, nearest.y); }
  }
  previousFrame = current;
  animationId = requestAnimationFrame(detectMotion);
}

function findClusters(mask) {
  const found = [];
  for (let y = 0; y < canvas.height; y += 8) for (let x = 0; x < canvas.width; x += 8) {
    let score = 0;
    for (let yy = y; yy < Math.min(y + 24, canvas.height); yy += 4) for (let xx = x; xx < Math.min(x + 24, canvas.width); xx += 4) score += mask[yy * canvas.width + xx];
    if (score > 5) found.push({ x: (x + 12) / canvas.width, y: (y + 12) / canvas.height, score });
  }
  return found.filter((item, index, all) => all.findIndex((other) => Math.hypot(item.x - other.x, item.y - other.y) < .08) === index).slice(0, 12);
}

function moveVirtualCursor(x, y) {
  centerBall.style.left = `${(1 - x) * 100}%`;
  centerBall.style.top = `${y * 100}%`;
}
