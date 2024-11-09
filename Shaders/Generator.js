// Importa el módulo fs para guardar el archivo
const fs = require('fs');

// Lee argumentos de línea de comandos
const args = process.argv.slice(2);
const numLados = parseInt(args[0], 10) || 8;
const radio = parseFloat(args[1]) || 1.0;
const ancho = parseFloat(args[2]) || 0.5;

// Validación de entradas
if (numLados < 3 || numLados > 360 || radio <= 0 || ancho <= 0) {
  console.error("Error: Los valores deben ser: numLados (3-360), radio (>0), ancho (>0)");
  process.exit(1);
}

// Generación de vértices
const vertices = [];
for (let i = 0; i < numLados; i++) {
  const angle = (2 * Math.PI * i) / numLados;
  const x = radio * Math.cos(angle);
  const z = radio * Math.sin(angle);
  vertices.push(`v ${(ancho / 2).toFixed(4)} ${x.toFixed(4)} ${z.toFixed(4)}`);
  vertices.push(`v -${(ancho / 2).toFixed(4)} ${x.toFixed(4)} ${z.toFixed(4)}`);
}
vertices.push(`v ${(ancho/2).toFixed(4)} 0.0000  0.0000 `);
vertices.push(`v ${-(ancho/2).toFixed(4)} 0.0000 0.0000 `);

// Generación de caras
const faces = [];
for (let i = 1; i <= numLados; i++) {
  const next = (i % numLados) + 1;
  faces.push(`f ${i * 2} ${next * 2 - 1} ${i * 2 - 1}`);
  faces.push(`f ${i * 2} ${next * 2} ${next * 2 - 1}`);
}
//Un lado de la rueda con numeros nones
for (let i = 1; i <= numLados*2; i+=2) {
    if (i+2 == numLados*2+1){
        faces.push(`f ${(numLados*2)+1} ${i} 1`);
        break;
    }
    else faces.push(`f ${(numLados*2)+1} ${i} ${i+2}`);
}
//Otro lado de la rueda con numeros pares
for (let i = numLados*2; i>=0; i-=2) {
    if (i == 2){
        faces.push(`f ${(numLados*2)+2} ${i} ${numLados*2}`);
        break;
    }
    faces.push(`f ${(numLados*2)+2} ${i} ${i-2}`);
}





// Estructura del archivo OBJ
const objData = [
  "# OBJ file",
  `# Vertices: ${vertices.length}`,
  ...vertices,
  `# Faces: ${faces.length}`,
  ...faces,
].join('\n');

// Guarda el archivo
fs.writeFileSync('wheel.obj', objData);
console.log("Archivo 'wheel.obj' generado con éxito.");
