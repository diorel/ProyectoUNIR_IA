// Importar dependencias
import express from 'express';
import dotenv from 'dotenv';
import axios from 'axios'; // Usaremos axios para realizar la petición HTTP

// Cargar configuración de variables de entorno
dotenv.config();

// Inicializar express
const app = express();
const PORT = process.env.PORT || 3000;

// Servir frontend
app.use("/", express.static("public"));

// Middleware para procesar JSON
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Contexto inicial para el chatbot
const contexto = `
Eres un asistente de dudas académicas, Para la escuela UNIR.
Información del negocio:
    - Ubicación: Madrid, España
    - Horario: Lunes a Viernes de 9:00 a 18:00
    - Carreras: Ingeniería Informática, Administración de Empresas, Psicología, Derecho, Medicina
    - Papeles importantes: acta de nacimiento, certificado de estudios, identificación oficial
    - Costos de inscripción: 100
    - Costo semestre: 5000
    - Costo mensualidad: 1000
    - Pagos: efectivo, tarjeta de crédito, transferencia bancaria
Solo puedes preguntar preguntas relacionadas con la escuela UNIR, no puedes hacer preguntas sobre otros temas.
`;

let conversations = {};

// Endpoint para manejar las solicitudes del chatbot
app.post("/api/chatbot", async (req, res) => {
    const { userId, message } = req.body;

    // Validar que el mensaje no esté vacío
    if (!message) {
        return res.status(400).json({ error: "Has mandado un mensaje vacío!!" });
    }

    // Inicializar la conversación si no existe
    if (!conversations[userId]) {
        conversations[userId] = [
            { role: "system", content: contexto },
            { role: "user", content: "Debes de responder de la forma más corta posible, usando los mínimos tokens posibles" },
        ];
    }

    // Agregar el mensaje del usuario a la conversación
    conversations[userId].push({ role: "user", content: message });

    try {
        // Petición a la API externa
        const response = await axios.post("http://localhost:8000/query", {
            question: message,
        });

        // Obtener la respuesta de la API
        const reply = response.data.response || "No se pudo obtener una respuesta.";

        // Agregar la respuesta del asistente a la conversación
        conversations[userId].push({ role: "assistant", content: reply });

        // Limitar el número de mensajes en la conversación
        if (conversations[userId].length > 10) {
            conversations[userId] = conversations[userId].slice(-10);
        }

        return res.status(200).json({ reply });
    } catch (error) {
        console.error("Error:", error.message);
        return res.status(500).json({ error: "Error al procesar la solicitud" });
    }
});

// Iniciar el servidor
app.listen(PORT, () => {
    console.log("Server is running on port " + PORT);
});