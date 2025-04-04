// Seleccionar elementos
const dropArea = document.getElementById("drop-area");
const imageUpload = document.getElementById("imageUpload");
const preview = document.getElementById("preview");

const btnProcesarImagen = document.getElementById('btnProcesarImagen');
const vehicleInfo = document.getElementById('vehicleInfo');
const alertGestion = document.getElementById('alertGestion');

// Función para mostrar vista previa
function showPreview(file) {
  const reader = new FileReader();
  reader.onload = function (e) {
    preview.src = e.target.result;
    preview.style.display = "block";

    btnProcesarImagen.disabled = false;
    if (vehicleInfo) vehicleInfo.style.display = 'none';
    if (alertGestion) alertGestion.style.display = 'none';
  };
  reader.readAsDataURL(file);
}

function loadingImage() {
  btnProcesarImagen.disabled = true;
  btnProcesarImagen.innerHTML = '<i class="fa fa-circle-notch fa-spin"></i>';
}

// Evento de arrastrar sobre el área
dropArea.addEventListener("dragover", function (e) {
  e.preventDefault();
  dropArea.style.backgroundColor = "#f0f0f0";
});

// Evento de salir del área de arrastre
dropArea.addEventListener("dragleave", function (e) {
  e.preventDefault();
  dropArea.style.backgroundColor = "#f9f9f9";
});

// Evento de soltar el archivo
dropArea.addEventListener("drop", function (e) {
  e.preventDefault();
  dropArea.style.backgroundColor = "#f9f9f9";
  const files = e.dataTransfer.files;
  if (files.length) {
    imageUpload.files = files; // Establecer los archivos seleccionados
    showPreview(files[0]);
  }
});

// Cuando el usuario hace clic en el área, abrir el selector de archivos
dropArea.addEventListener("click", function () {
  imageUpload.click();
});

// Cuando el usuario selecciona un archivo mediante el input
imageUpload.addEventListener("change", function () {
  const file = imageUpload.files[0];
  if (file) {
    showPreview(file);
  }
});
