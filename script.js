const video = document.getElementById("webcam");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const resultado = document.getElementById("resultado");
async function iniciarCamara() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
  } catch (error) {
    resultado.innerText = "❌ No se pudo acceder a la cámara";
    console.error(error);
  }
}
async function verificarRostro() {
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const dataURL = canvas.toDataURL("image/jpeg");
  const base64 = dataURL.split(',')[1];

  resultado.innerText = "⏳ Verificando rostro...";

  const res = await fetch("/verificar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ imagen: base64 })
  });

  const data = await res.json();
  if (data.error) {
    resultado.innerText = "⚠️ Error: " + data.error;
  } else {
    resultado.innerText = `${data.mensaje} (Distancia: ${data.distancia.toFixed(4)})`;
  }
}
iniciarCamara();