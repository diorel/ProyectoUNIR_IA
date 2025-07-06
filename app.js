// Importar dependecias
import express from 'express';
import dotenv from 'dotenv';
import OpenAI from 'openai';
import ollama from 'ollama'

// cargar configuracion (de api key)

dotenv.config();

// cargar expressde
const app = express();
const PORT = process.env.PORT || 3000;

// servir frontend
app.use("/", express.static("public"));

// Middleware para procesar json
app.use(express.json());
app.use(express.urlencoded({extended: true}));

// Instancia de openia y pasar el api key

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

// Ruta / endponint / url

const contexto = `
Eres un asistente de dudas academicas, Para la escuela UNIR.
Informacion del negocio:
    - Ubicacion: Madrid, España
    - Horario: Lunes a Viernes de 9:00 a 18:00
    - Carreras: Ingenieria Informatica, Administracion de Empresas, Psicologia, Derecho , Medicina
    - Papeles importantes: acta de nacimiento, certificado de estudios, identificacion oficial
    - Costos de inscripcion: 100
    - costo semestre: 5000,
    - Costo mensualidad: 1000
    - Pagos: efectivo, tarjeta de credito, transferencia bancaria
Solo puedes preguntar preguntas relacionadas con la escuela UNIR, no puedes hacer preguntas sobre otros temas.
`;

let contversations = {}; 

app.post("/api/chatbot", async (req, res) => {



     // Recibir pregunta del usuario

     const { userId, message } = req.body;

     if(!contversations[userId]){
        contversations[userId] = [
            {role: "system", content: contexto},
            {role: "user", content: "Debes de responder de la forma mas corta posible, Usando los minimos tokens posibles"},
        ];
     }

     contversations[userId].push({role: "user", content: message});

    
     if(!message) return res.status(400).json({error: "Has mandado un mensaje vacio!!"});

     // Peticion al modelo de inteligancia artificial

     try{

        const response = await openai.chat.completions.create({
            model: "gpt-3.5-turbo",
            messages: contversations[userId],
            max_tokens: 200
        });

        // Devolver respuesta   
        const reply = response.choices[0].message.content;


        // AÑADIR AL ASISTENTE LA RESPUESTA
        contversations[userId].push({role: "assistant", content: reply});

        //Limitar numero de mensajes
        if(contversations[userId].length > 10) {
            contversations[userId] = contversations[userId].slice(-10);
        }
        
        return res.status(200).json({reply});


     }catch (error) {
        console.error("Error:", error);
        
        return res.status(500).json({error: "Error al procesar la solicitud"});
     }


     // Devolver respuesta 

});

app.post('/api/llama', async (req, res) => {
    const { message } = req?.body;

    const messages = [
        {
            role: 'system',
            content: contexto
        },
        { role: 'user', content: message }
    ];


    const response = await ollama.chat({
        model: 'llama3.2',
        messages
    });

    return res.status(200).json({reply: response?.message?.content});
});



// Servir el Backend
app.listen(PORT, () => {
    console.log("Server is running on port" + PORT);
});