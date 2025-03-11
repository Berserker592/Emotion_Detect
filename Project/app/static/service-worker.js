let ws;
let path = 'https://emotionvisia.com';

self.addEventListener("activate", event => {
    event.waitUntil(startWebSocket());
});

function startWebSocket() {
    ws = new WebSocket(`wss://${path2}/ws`);

    ws.onmessage = event => {
        // Enviar mensajes a la pestaña activa
        self.clients.matchAll().then(clients => {
            clients.forEach(client => client.postMessage(event.data));
        });
    };

    ws.onclose = () => {
        console.log("WebSocket cerrado. Reconectando...");
        setTimeout(startWebSocket, 1000); // Reconectar después de 1 segundo
    };
}