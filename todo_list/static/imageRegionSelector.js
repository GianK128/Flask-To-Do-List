const preview = document.querySelector('[pic-preview]');
const picInput = document.querySelector('[pic-input]');
const picWrapper = document.querySelector('.pic-preview-wrapper');
const picHelp = document.querySelector('.pic-preview-help');
const picCutValues = document.querySelector('[pic-cut]');
const picFilename = document.querySelector('.pic-filename');

const clamp = (num, min, max) => { return Math.min(Math.max(num, min), max) }

// IMAGE DRAG & DROP

picWrapper.addEventListener('dragover', e => {
  e.preventDefault();
  picHelp.classList.add('drag-over');
});

['dragleave', 'dragend'].forEach(ev => {
  picWrapper.addEventListener(ev , e => {
    picHelp.classList.remove('drag-over');
  });
});

picWrapper.addEventListener('drop', e => {
  e.preventDefault();

  if (e.dataTransfer.files.length) {
    picInput.files = e.dataTransfer.files;
    CreatePicPreview();
  }
});

// IMAGE PREVIEW

picHelp.addEventListener('click', e => {
  picInput.click();
});

picInput.addEventListener('change', (e) => {
  CreatePicPreview();
});

function CreatePicPreview() {
  // Agregar nombre de archivo
  picFilename.textContent = picInput.files[0].name;

  // Borrar prompt de Drag&Drop
  picHelp.remove();

  // Limpiar en caso de que haya otra imagen
  preview.innerHTML = "";
  picCutValues.value = "";
  
  // Leer archivo y ver si es una imagen
  const file = picInput.files[0];
  if (!file.type.startsWith('image/')){ console.log("ERROR DIABOLICO") }

  // Crear elemento img en el DOM
  const img = document.createElement("img");
  img.file = file;
  preview.appendChild(img);

  // Crear elemento div usado como selector
  const selector = document.createElement('div');
  selector.classList.add('image-selector');

  let mouseOffset, maxOffset;
  let isPressed = false;
  let maxRefX, maxRefY, refX, refY;

  // Eventos para saber si esta presionado o no
  selector.addEventListener('mousedown', (e) => {
    isPressed = true;
    mouseOffset = e.clientX - e.target.offsetLeft;
    maxOffset = e.target.parentNode.clientWidth - e.target.offsetWidth;
  });
  selector.addEventListener('mouseup', () => {
    isPressed = false;
  });

  // Logica para moverlo a lo largo del contenedor
  selector.addEventListener('mousemove', (e) => {
    e.preventDefault();

    if (isPressed) {
      let newOffSet = clamp(e.clientX - mouseOffset, 0, maxOffset)
      e.target.style.left = `${newOffSet}px`

      console.log(refX, refY, maxRefX, maxRefY);

      // Escribir valores para pasar al backend en un input
      let values = [
        ReglaDeTres(refX, maxRefX, newOffSet),
        ReglaDeTres(refY, maxRefY, e.target.offsetTop),
        ReglaDeTres(refX, maxRefX, newOffSet + e.target.offsetWidth),
        ReglaDeTres(refY, maxRefY, e.target.offsetTop + e.target.clientHeight)
      ]
      picCutValues.value = `${values.join('-')}`
    }
  });

  // Agregarlo al DOM
  preview.appendChild(selector);

  // Asegurarse que el selector no se extienda si cambia el tama??o de la ventana
  window.addEventListener('resize', () => {
    refX = preview.clientWidth;
    refY = preview.clientHeight;
    let newMaxOffset = refX - selector.offsetWidth;
    selector.style.left = `${Math.min(selector.style.left.slice(0, -2), newMaxOffset)}px`
  })

  // Leer imagen y cargarla en el elemento
  // Calcular referencia para enviar al backend
  const reader = new FileReader();
  reader.onload = (function(aImg) {
    return function(e) {
      let image = new Image();
      image.src = reader.result;
      image.onload = function () {
        if (this.width < 600 || this.height < 600) {
          alert("Por favor, ingrese una imagen de 600x600px como m??nimo.");
        }
        
        maxRefX = this.width;
        maxRefY = this.height;

        aImg.src = e.target.result; 

        refX = preview.clientWidth;
        refY = preview.clientHeight;

        let values = [
          ReglaDeTres(refX, maxRefX, selector.offsetLeft),
          ReglaDeTres(refY, maxRefY, selector.offsetTop),
          ReglaDeTres(refX, maxRefX, selector.offsetLeft + selector.offsetWidth),
          ReglaDeTres(refY, maxRefY, selector.offsetTop + selector.clientHeight)
        ]
        picCutValues.value = `${values.join('-')}`;
      }
    }; 
  })(img);
  reader.readAsDataURL(file);
}

function ReglaDeTres(currentMax, previousMax, currentValue) {
  return Math.floor((currentValue * previousMax) / currentMax);
}