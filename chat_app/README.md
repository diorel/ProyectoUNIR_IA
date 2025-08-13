# Chat de Dudas Académicas - UNIR

Este proyecto es una aplicación de chat diseñada para resolver dudas académicas entre estudiantes y tutores de UNIR, facilitando la comunicación en tiempo real. La aplicación utiliza un backend basado en Node.js y Express, y un frontend interactivo con HTML, CSS y JavaScript.

## 📋 Funcionalidad

- **Interfaz de usuario moderna**: Diseño responsivo y accesible para interactuar con el chatbot.
- **Chatbot académico**: Responde preguntas relacionadas con la universidad UNIR, como horarios, costos y requisitos.
- **Integración con API externa**: El chatbot se conecta a un sistema RAG (Retrieval Augmented Generation) para obtener respuestas basadas en documentos específicos.
- **Mensajes en tiempo real**: Simulación de mensajes con animaciones de carga.

## 📦 Dependencias

El proyecto utiliza las siguientes librerías y herramientas:

### Dependencias principales:

- **[axios](https://www.npmjs.com/package/axios)**: Para realizar solicitudes HTTP al backend del sistema RAG.
- **[dotenv](https://www.npmjs.com/package/dotenv)**: Para manejar variables de entorno de manera segura.
- **[express](https://www.npmjs.com/package/express)**: Framework para construir el servidor backend.
- **[openai](https://www.npmjs.com/package/openai)**: Librería para interactuar con la API de OpenAI.

### Dependencias de desarrollo:

- **[nodemon](https://www.npmjs.com/package/nodemon)**: Herramienta para reiniciar automáticamente el servidor durante el desarrollo.

## 🚀 Instalación

Sigue estos pasos para instalar y levantar el proyecto:

1. Clonar el repositorio
   Clona este repositorio en tu máquina local:

```bash
git clone <URL_DEL_REPOSITORIO>
cd chat_app
```

2. Instalar dependencias

Asegúrate de tener Node.js instalado. Luego, instala las dependencias del proyecto:

```bash
npm install
```

3. Configurar variables de entorno

Crea un archivo .env en la raíz del proyecto y define las variables necesarias. Por ejemplo:

PORT=3000

### 4. Levantar el servidor

```bash
npm start
```

Para iniciar el servidor en modo producción:

```bash
npm run serve
```

### 5. Acceder a la aplicación

Abre tu navegador y accede a http://localhost:3000.

chat*app/
├── public/
│ ├── assets/
│ │ ├── css/
│ │ │ └── [styles.css](http://\_vscodecontentref*/0) ) # Estilos del frontend
│ │ ├── js/
│ │ │ └── [`chat_app/public/assets/js/main.js`](chat_app/public/assets/js/main.js) # Lógica del frontend
│ │ └── img/
│ │ └── icon-unir.png # Icono de la aplicación
│ └── [`chat_app/public/index.html`](chat_app/public/index.html) # Interfaz principal
├── [`chat_app/app.js`](chat_app/app.js) # Servidor backend
├── [`chat_app/package.json`](chat_app/package.json) # Configuración del proyecto
└── .env # Variables de entorno
