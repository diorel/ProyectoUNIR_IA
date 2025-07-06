# Chat de Dudas Académicas - UNIR

Este proyecto es un chat diseñado para resolver dudas académicas entre estudiantes y tutores de UNIR, facilitando la comunicación en tiempo real.

## 📦 Instalación

Para instalar las dependencias del proyecto, ejecuta el siguiente comando:

```bash
npm install
```

Ve a la siguiente pagina y descarga ollama: `https://ollama.com/download/windows`

ejecuta:

```bash
ollama run llama3.2
```

Es necesario crear un archivo .env, puedes usar el .env.template

despues puedes correr la app con:

```bash
node app.js
```

ve a la pagina:

```
http://localhost:3000/
```

para usar ollama agrega el query param `?llm=llama`

```
 http://localhost:3000/?llm=llama
```
