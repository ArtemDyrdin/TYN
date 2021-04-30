// при создании переменных в современном js не следует использовать ключевое слово var
// для переменных, которые не будут меняться нужно использовать ключевое слово const
// для переменных, которые собираешься переопределять следует использовать ключевое слово let


// находим на странице кусок html по id. В данном случае - видео
const video = document.querySelector("#videoElement");

// получаем картинку с веб камеры
if (navigator.mediaDevices.getUserMedia) {
navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
        console.log('strem: ', stream.getVideoTracks());
        video.srcObject = stream; // если все ок, то полученное видео передаем в тег видео для показа пользователю
    })
    .catch(function (error) { // если не ок, то выводим в консоль ошибку
        console.log("Something went wrong!", error.data);
    });
}

const getFrame = () => {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    const data = canvas.toDataURL('image/png');
    return data;
}

const FPS = 3;

const url = 'ws://localhost:5000';

const socket = new WebSocket(url);

// Connection opened
socket.addEventListener('open', function (event) {
    console.log('Connected to the WS Server!')
});

// Connection closed
socket.addEventListener('close', function (event) {
    console.log('Disconnected from the WS Server!')
});

// Listen for messages
socket.addEventListener('message', function (event) {
    console.log('Message from server ', event.data);
});
// Send a msg to the websocket
const sendMsg = () => {
    socket.send('Hello from Client2!');
}
// test of input
function a_value(data){
    socket.send(data.value);
}
socket.addEventListener('Message', (event) => {
    console.log(event.data);
});

socket.onopen = () => {
    console.log(`Connected to ${url}`);
    setInterval(() => {
        socket.send(getFrame());
    }, 1000 / FPS);
}
