// находим на странице кусок html по id. В данном случае - видео
const video = document.querySelector("#videoElement");
const controls = document.querySelector("#controls");
let intervalId;
const FPS = 3;

// поучить кадр
const getFrame = () => {
  console.log('get frame');
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  const data = canvas.toDataURL('image/png');
  return data;
};


// прекратить отправку кадров
function endWorkout() {
  console.log('end workout clicked!');
  clearInterval(intervalId);
};

const getUserVideo = () => {
  if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function (stream) {
        console.log('camera is active');
        controls.style.display = 'block';
        console.log('strem: ', stream.getVideoTracks());
        // если все ок, то полученное видео передаем в тег видео для показа пользователю
        video.srcObject = stream;
      })
      // если не ок, то выводим в консоль ошибку
      .catch(function (error) { 
        console.log("Something went wrong!", error.data);
      });
    };
};
