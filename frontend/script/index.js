// находим на странице кусок html по id. В данном случае - видео
const video = document.querySelector("#videoElement");
const controls = document.querySelector("#controls");
let intervalId;

// получаем картинку с веб камеры
if (navigator.mediaDevices.getUserMedia) {
navigator.mediaDevices.getUserMedia({ video: true })
  .then(function (stream) {
    console.log('camera is active');
    controls.style.display = 'block';
    console.log('strem: ', stream.getVideoTracks());
    video.srcObject = stream; // если все ок, то полученное видео передаем в тег видео для показа пользователю
  })
  .catch(function (error) { // если не ок, то выводим в консоль ошибку
    console.log("Something went wrong!", error.data);
  });
}

const getFrame = () => {
  console.log('get frame');
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  const data = canvas.toDataURL('image/png');
  return data;
}

const FPS = 0.1;

const url = 'ws://localhost:5000';

const socket = new WebSocket(url);

// Connection opened
socket.addEventListener('open', function (event) {
  console.log('Socket is opened!');
});

// Connection closed
socket.addEventListener('close', function (event) {
  console.log('Socket is closed!');
});

// Listen for messages
socket.addEventListener('message', function (event) {
  console.log('Message from server: ', event.data);
});

// Listen for errors
socket.onerror = function(error) {
  console.log('Websocket error: ', error.message);
};

socket.onopen = () => {
  console.log(`Connected to ${url}`);
  startWorkout();
}

// начать отправку кадров по клику
function startWorkout() {
  console.log('start workout clicked!');
  intervalId = setInterval(() => {
    socket.send(getFrame());
  }, 1000 / FPS);
}

// прекратить отправку кадров по клику
function endWorkout() {
  console.log('end workout clicked!');
  clearInterval(intervalId);
}
