function abrirPanel() {

  document.getElementById("panelModal").style.display = "flex";

}

function cerrarPanel() {

  document.getElementById("panelModal").style.display = "none";

}

function volverLista(){

  document.getElementById("estadisticasDia").style.display="none";

  document.querySelector(".lista-fechas").style.display="grid";

}

const datos={

"2026-03-02":{

leche:{
reclamados:186,
noReclamados:8,
regalados:6
},

almuerzo:{
reclamados:94,
noReclamados:4,
regalados:2
},

asistencia:{
presentes:95,
ausentes:5
},

estudiantes:[
"Juan Pérez",
"Camila Gómez"
]

},

"2026-03-03":{

leche:{
reclamados:182,
noReclamados:12,
regalados:6
},

almuerzo:{
reclamados:92,
noReclamados:5,
regalados:3
},

asistencia:{
presentes:94,
ausentes:6
},

estudiantes:[
"Laura Ruiz",
"Andrés Soto"
]

},

"2026-03-04":{

leche:{
reclamados:188,
noReclamados:7,
regalados:5
},

almuerzo:{
reclamados:95,
noReclamados:3,
regalados:2
},

asistencia:{
presentes:97,
ausentes:3
},

estudiantes:[
"María López"
]

},

"2026-03-05":{

leche:{
reclamados:184,
noReclamados:10,
regalados:6
},

almuerzo:{
reclamados:93,
noReclamados:4,
regalados:3
},

asistencia:{
presentes:95,
ausentes:5
},

estudiantes:[
"Daniel Toro",
"Valentina Díaz"
]

},

"2026-03-06":{

leche:{
reclamados:190,
noReclamados:5,
regalados:5
},

almuerzo:{
reclamados:98,
noReclamados:1,
regalados:1
},

asistencia:{
presentes:98,
ausentes:2
},

estudiantes:[
"Samuel Ruiz"
]

},

"2026-03-09":{

leche:{
reclamados:183,
noReclamados:11,
regalados:6
},

almuerzo:{
reclamados:91,
noReclamados:6,
regalados:3
},

asistencia:{
presentes:94,
ausentes:6
},

estudiantes:[
"Juliana Gil",
"Mateo Ortiz"
]

},

"2026-03-10":{

leche:{
reclamados:187,
noReclamados:8,
regalados:5
},

almuerzo:{
reclamados:96,
noReclamados:2,
regalados:2
},

asistencia:{
presentes:97,
ausentes:3
},

estudiantes:[
"Isabella Pérez"
]

},

"2026-03-11":{

leche:{
reclamados:181,
noReclamados:13,
regalados:6
},

almuerzo:{
reclamados:90,
noReclamados:7,
regalados:3
},

asistencia:{
presentes:93,
ausentes:7
},

estudiantes:[
"Juan Castro",
"Lucía Ramírez"
]

},

"2026-03-12":{

leche:{
reclamados:185,
noReclamados:9,
regalados:6
},

almuerzo:{
reclamados:94,
noReclamados:4,
regalados:2
},

asistencia:{
presentes:96,
ausentes:4
},

estudiantes:[
"Carlos Mejía"
]

},

"2026-03-13":{

leche:{
reclamados:189,
noReclamados:6,
regalados:5
},

almuerzo:{
reclamados:97,
noReclamados:2,
regalados:1
},

asistencia:{
presentes:98,
ausentes:2
},

estudiantes:[
"Valeria Gómez"
]

},

"2026-03-16":{

leche:{
reclamados:184,
noReclamados:10,
regalados:6
},

almuerzo:{
reclamados:93,
noReclamados:5,
regalados:2
},

asistencia:{
presentes:95,
ausentes:5
},

estudiantes:[
"Juan David Rojas",
"María López"
]

},

"2026-03-17":{

leche:{
reclamados:188,
noReclamados:7,
regalados:5
},

almuerzo:{
reclamados:96,
noReclamados:2,
regalados:2
},

asistencia:{
presentes:97,
ausentes:3
},

estudiantes:[
"Sofía Gómez"
]

},

"2026-03-18":{

leche:{
reclamados:182,
noReclamados:12,
regalados:6
},

almuerzo:{
reclamados:91,
noReclamados:6,
regalados:3
},

asistencia:{
presentes:94,
ausentes:6
},

estudiantes:[
"Camilo Ruiz",
"Laura Díaz"
]

},

"2026-03-19":{

leche:{
reclamados:190,
noReclamados:5,
regalados:5
},

almuerzo:{
reclamados:98,
noReclamados:1,
regalados:1
},

asistencia:{
presentes:99,
ausentes:1
},

estudiantes:[
"Valentina Pérez"
]

},

"2026-03-20":{

leche:{
reclamados:186,
noReclamados:8,
regalados:6
},

almuerzo:{
reclamados:94,
noReclamados:4,
regalados:2
},

asistencia:{
presentes:96,
ausentes:4
},

estudiantes:[
"Mateo Giraldo"
]

},

"2026-03-23":{

leche:{
reclamados:183,
noReclamados:11,
regalados:6
},

almuerzo:{
reclamados:92,
noReclamados:5,
regalados:3
},

asistencia:{
presentes:94,
ausentes:6
},

estudiantes:[
"Isabella Ruiz",
"Carlos Sánchez"
]

},

"2026-03-24":{

leche:{
reclamados:187,
noReclamados:8,
regalados:5
},

almuerzo:{
reclamados:95,
noReclamados:3,
regalados:2
},

asistencia:{
presentes:97,
ausentes:3
},

estudiantes:[
"Daniela Gómez"
]

},

"2026-03-25":{

leche:{
reclamados:185,
noReclamados:9,
regalados:6
},

almuerzo:{
reclamados:93,
noReclamados:4,
regalados:3
},

asistencia:{
presentes:95,
ausentes:5
},

estudiantes:[
"Juan Esteban Pérez"
]

},

"2026-03-26":{

leche:{
reclamados:189,
noReclamados:6,
regalados:5
},

almuerzo:{
reclamados:97,
noReclamados:2,
regalados:1
},

asistencia:{
presentes:98,
ausentes:2
},

estudiantes:[
"Paula Martínez"
]

},

"2026-03-27":{

leche:{
reclamados:181,
noReclamados:13,
regalados:6
},

almuerzo:{
reclamados:90,
noReclamados:7,
regalados:3
},

asistencia:{
presentes:93,
ausentes:7
},

estudiantes:[
"Samuel Restrepo",
"Ana Torres"
]

},

"2026-03-30":{

leche:{
reclamados:184,
noReclamados:10,
regalados:6
},

almuerzo:{
reclamados:94,
noReclamados:4,
regalados:2
},

asistencia:{
presentes:95,
ausentes:5
},

estudiantes:[
"Laura Gómez",
"Juan Pérez"
]

},

"2026-03-31":{

leche:{
reclamados:188,
noReclamados:7,
regalados:5
},

almuerzo:{
reclamados:96,
noReclamados:2,
regalados:2
},

asistencia:{
presentes:97,
ausentes:3
},

estudiantes:[
"Carlos Ruiz"
]

},

"2026-04-01":{

leche:{
reclamados:185,
noReclamados:9,
regalados:6
},

almuerzo:{
reclamados:93,
noReclamados:5,
regalados:2
},

asistencia:{
presentes:95,
ausentes:5
},

estudiantes:[
"María López"
]

},

"2026-04-06":{

leche:{
reclamados:190,
noReclamados:5,
regalados:5
},

almuerzo:{
reclamados:98,
noReclamados:1,
regalados:1
},

asistencia:{
presentes:99,
ausentes:1
},

estudiantes:[
"Valentina Gómez"
]

},

"2026-04-07":{

leche:{
reclamados:183,
noReclamados:11,
regalados:6
},

almuerzo:{
reclamados:92,
noReclamados:5,
regalados:3
},

asistencia:{
presentes:94,
ausentes:6
},

estudiantes:[
"Andrés Martínez",
"Sofía Ruiz"
]

},

"2026-04-08":{

leche:{
reclamados:187,
noReclamados:8,
regalados:5
},

almuerzo:{
reclamados:95,
noReclamados:3,
regalados:2
},

asistencia:{
presentes:97,
ausentes:3
},

estudiantes:[
"Camilo Torres"
]

},

"2026-04-09":{

leche:{
reclamados:182,
noReclamados:12,
regalados:6
},

almuerzo:{
reclamados:91,
noReclamados:6,
regalados:3
},

asistencia:{
presentes:94,
ausentes:6
},

estudiantes:[
"Juliana Díaz",
"Mateo Gómez"
]

},

"2026-04-10":{

leche:{
reclamados:189,
noReclamados:6,
regalados:5
},

almuerzo:{
reclamados:97,
noReclamados:2,
regalados:1
},

asistencia:{
presentes:98,
ausentes:2
},

estudiantes:[
"Daniel Restrepo"
]

},

"2026-04-13":{

leche:{
reclamados:186,
noReclamados:8,
regalados:6
},

almuerzo:{
reclamados:94,
noReclamados:4,
regalados:2
},

asistencia:{
presentes:96,
ausentes:4
},

estudiantes:[
"Laura Gómez",
"Juan Restrepo"
]

},

"2026-04-14":{

leche:{
reclamados:184,
noReclamados:10,
regalados:6
},

almuerzo:{
reclamados:93,
noReclamados:5,
regalados:2
},

asistencia:{
presentes:95,
ausentes:5
},

estudiantes:[
"Valentina Ruiz"
]

},

"2026-04-15":{

leche:{
reclamados:190,
noReclamados:5,
regalados:5
},

almuerzo:{
reclamados:98,
noReclamados:1,
regalados:1
},

asistencia:{
presentes:99,
ausentes:1
},

estudiantes:[
"Camilo Pérez"
]

},

"2026-04-16":{

leche:{
reclamados:181,
noReclamados:13,
regalados:6
},

almuerzo:{
reclamados:90,
noReclamados:7,
regalados:3
},

asistencia:{
presentes:93,
ausentes:7
},

estudiantes:[
"Sara Gómez",
"Daniel Ruiz"
]

},

"2026-04-17":{

leche:{
reclamados:188,
noReclamados:7,
regalados:5
},

almuerzo:{
reclamados:96,
noReclamados:2,
regalados:2
},

asistencia:{
presentes:97,
ausentes:3
},

estudiantes:[
"María López"
]

},

"2026-04-20":{

leche:{
reclamados:183,
noReclamados:11,
regalados:6
},

almuerzo:{
reclamados:92,
noReclamados:5,
regalados:3
},

asistencia:{
presentes:94,
ausentes:6
},

estudiantes:[
"Andrés Soto",
"Paula Díaz"
]

},

"2026-04-21":{

leche:{
reclamados:187,
noReclamados:8,
regalados:5
},

almuerzo:{
reclamados:95,
noReclamados:3,
regalados:2
},

asistencia:{
presentes:97,
ausentes:3
},

estudiantes:[
"Juan Pablo Ruiz"
]

},

"2026-04-22":{

leche:{
reclamados:185,
noReclamados:9,
regalados:6
},

almuerzo:{
reclamados:94,
noReclamados:4,
regalados:2
},

asistencia:{
presentes:96,
ausentes:4
},

estudiantes:[
"Isabella Gómez"
]

},

"2026-04-23":{

leche:{
reclamados:189,
noReclamados:6,
regalados:5
},

almuerzo:{
reclamados:97,
noReclamados:2,
regalados:1
},

asistencia:{
presentes:98,
ausentes:2
},

estudiantes:[
"Samuel Restrepo"
]

},

"2026-04-24":{

leche:{
reclamados:182,
noReclamados:12,
regalados:6
},

almuerzo:{
reclamados:91,
noReclamados:6,
regalados:3
},

asistencia:{
presentes:94,
ausentes:6
},

estudiantes:[
"Camila Torres",
"David Pérez"
]

},

"2026-04-27":{

leche:{
reclamados:186,
noReclamados:8,
regalados:6
},

almuerzo:{
reclamados:94,
noReclamados:4,
regalados:2
},

asistencia:{
presentes:96,
ausentes:4
},

estudiantes:[
"Laura Martínez",
"Carlos Gómez"
]

},

"2026-04-28":{

leche:{
reclamados:184,
noReclamados:10,
regalados:6
},

almuerzo:{
reclamados:93,
noReclamados:5,
regalados:2
},

asistencia:{
presentes:95,
ausentes:5
},

estudiantes:[
"Valentina Ruiz"
]

},

"2026-04-29":{

leche:{
reclamados:188,
noReclamados:7,
regalados:5
},

almuerzo:{
reclamados:96,
noReclamados:2,
regalados:2
},

asistencia:{
presentes:97,
ausentes:3
},

estudiantes:[
"Juan David Pérez"
]

},

"2026-04-30":{

leche:{
reclamados:183,
noReclamados:11,
regalados:6
},

almuerzo:{
reclamados:92,
noReclamados:5,
regalados:3
},

asistencia:{
presentes:94,
ausentes:6
},

estudiantes:[
"Sofía Gómez",
"Andrés Ruiz"
]

},

"2026-05-04":{

leche:{
reclamados:190,
noReclamados:5,
regalados:5
},

almuerzo:{
reclamados:98,
noReclamados:1,
regalados:1
},

asistencia:{
presentes:99,
ausentes:1
},

estudiantes:[
"María López"
]

},

"2026-05-05":{

leche:{
reclamados:185,
noReclamados:9,
regalados:6
},

almuerzo:{
reclamados:94,
noReclamados:4,
regalados:2
},

asistencia:{
presentes:96,
ausentes:4
},

estudiantes:[
"Camilo Restrepo"
]

},

"2026-05-06":{

leche:{
reclamados:182,
noReclamados:12,
regalados:6
},

almuerzo:{
reclamados:91,
noReclamados:6,
regalados:3
},

asistencia:{
presentes:94,
ausentes:6
},

estudiantes:[
"Paula Díaz",
"Daniel Gómez"
]

},

"2026-05-07":{

leche:{
reclamados:189,
noReclamados:6,
regalados:5
},

almuerzo:{
reclamados:97,
noReclamados:2,
regalados:1
},

asistencia:{
presentes:98,
ausentes:2
},

estudiantes:[
"Juan Torres"
]

},

"2026-05-08":{

leche:{
reclamados:186,
noReclamados:8,
regalados:6
},

almuerzo:{
reclamados:95,
noReclamados:3,
regalados:2
},

asistencia:{
presentes:97,
ausentes:3
},

estudiantes:[
"Isabella Ruiz"
]

},

"2026-05-11":{

leche:{
reclamados:184,
noReclamados:10,
regalados:6
},

almuerzo:{
reclamados:93,
noReclamados:5,
regalados:2
},

asistencia:{
presentes:95,
ausentes:5
},

estudiantes:[
"Laura Gómez",
"Mateo Ruiz"
]

},

"2026-05-12":{

leche:{
reclamados:188,
noReclamados:7,
regalados:5
},

almuerzo:{
reclamados:96,
noReclamados:2,
regalados:2
},

asistencia:{
presentes:97,
ausentes:3
},

estudiantes:[
"Juan Pérez"
]

},

"2026-05-13":{

leche:{
reclamados:182,
noReclamados:12,
regalados:6
},

almuerzo:{
reclamados:91,
noReclamados:6,
regalados:3
},

asistencia:{
presentes:94,
ausentes:6
},

estudiantes:[
"Camila Torres",
"Samuel Díaz"
]

},

"2026-05-14":{

leche:{
reclamados:190,
noReclamados:5,
regalados:5
},

almuerzo:{
reclamados:98,
noReclamados:1,
regalados:1
},

asistencia:{
presentes:99,
ausentes:1
},

estudiantes:[
"Valentina Restrepo"
]

},

"2026-05-15":{

leche:{
reclamados:185,
noReclamados:9,
regalados:6
},

almuerzo:{
reclamados:94,
noReclamados:4,
regalados:2
},

asistencia:{
presentes:96,
ausentes:4
},

estudiantes:[
"Andrés Gómez"
]

},

"2026-05-18":{

leche:{
reclamados:187,
noReclamados:8,
regalados:5
},

almuerzo:{
reclamados:95,
noReclamados:3,
regalados:2
},

asistencia:{
presentes:97,
ausentes:3
},

estudiantes:[
"María Ruiz"
]

},

"2026-05-19":{

leche:{
reclamados:183,
noReclamados:11,
regalados:6
},

almuerzo:{
reclamados:92,
noReclamados:5,
regalados:3
},

asistencia:{
presentes:94,
ausentes:6
},

estudiantes:[
"Daniel Torres",
"Laura Pérez"
]

},

"2026-05-20":{

leche:{
reclamados:189,
noReclamados:6,
regalados:5
},

almuerzo:{
reclamados:97,
noReclamados:2,
regalados:1
},

asistencia:{
presentes:98,
ausentes:2
},

estudiantes:[
"Camilo Gómez"
]

},

"2026-05-21":{

leche:{
reclamados:186,
noReclamados:8,
regalados:6
},

almuerzo:{
reclamados:94,
noReclamados:4,
regalados:2
},

asistencia:{
presentes:96,
ausentes:4
},

estudiantes:[
"Juliana Ruiz"
]

},

"2026-05-22":{

leche:{
reclamados:184,
noReclamados:10,
regalados:6
},

almuerzo:{
reclamados:93,
noReclamados:5,
regalados:2
},

asistencia:{
presentes:95,
ausentes:5
},

estudiantes:[
"Valentina Gómez",
"Juan David Ruiz"
]

},

"2026-05-25":{

leche:{
reclamados:188,
noReclamados:7,
regalados:5
},

almuerzo:{
reclamados:96,
noReclamados:2,
regalados:2
},

asistencia:{
presentes:97,
ausentes:3
},

estudiantes:[
"Camila Torres"
]

},

"2026-05-26":{

leche:{
reclamados:182,
noReclamados:12,
regalados:6
},

almuerzo:{
reclamados:91,
noReclamados:6,
regalados:3
},

asistencia:{
presentes:94,
ausentes:6
},

estudiantes:[
"Mateo Restrepo",
"Laura Pérez"
]

},

"2026-05-27":{

leche:{
reclamados:189,
noReclamados:6,
regalados:5
},

almuerzo:{
reclamados:97,
noReclamados:2,
regalados:1
},

asistencia:{
presentes:98,
ausentes:2
},

estudiantes:[
"Andrés Gómez"
]

},

"2026-05-28":{

leche:{
reclamados:186,
noReclamados:8,
regalados:6
},

almuerzo:{
reclamados:95,
noReclamados:3,
regalados:2
},

asistencia:{
presentes:96,
ausentes:4
},

estudiantes:[
"Sofía Ruiz"
]

},

"2026-05-29":{

leche:{
reclamados:190,
noReclamados:5,
regalados:5
},

almuerzo:{
reclamados:98,
noReclamados:1,
regalados:1
},

asistencia:{
presentes:99,
ausentes:1
},

estudiantes:[
"Carlos Martínez"
]

}

};

function mostrarFecha(fecha){

const info=datos[fecha];

if(!info){

return;

}

document.querySelector(".lista-fechas").style.display="none";

document.getElementById("estadisticasDia").style.display="block";

document.getElementById("tituloFecha").innerHTML="📅 "+fecha.split("-").reverse().join("/");

document.getElementById("contenidoEstadisticas").innerHTML=`

<div class="tarjeta">

<h2>🥛 Vaso de leche</h2>

<p>Reclamados: ${info.leche.reclamados}</p>

<p>No reclamados: ${info.leche.noReclamados}</p>

<p>Regalados: ${info.leche.regalados}</p>

</div>

<div class="tarjeta">

<h2>🍽 Almuerzo</h2>

<p>Reclamados: ${info.almuerzo.reclamados}</p>

<p>No reclamados: ${info.almuerzo.noReclamados}</p>

<p>Regalados: ${info.almuerzo.regalados}</p>

</div>

<div class="tarjeta">

<h2>👥 Asistencia</h2>

<p>Presentes: ${info.asistencia.presentes}</p>

<p>Ausentes: ${info.asistencia.ausentes}</p>

<p><strong>Estudiantes que no reclamaron:</strong></p>

<ul>

${info.estudiantes.map(nombre=>`<li>${nombre}</li>`).join("")}

</ul>

</div>

`;

}

function volverLista(){

document.getElementById("estadisticasDia").style.display="none";

document.querySelector(".lista-fechas").style.display="grid";

document.getElementById("contenidoEstadisticas").innerHTML="";

document.getElementById("tituloFecha").innerHTML="";

}