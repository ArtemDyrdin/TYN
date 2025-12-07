const url = 'ws://localhost:5000';

const socket = new WebSocket(url);

let question = ""; // для хранения вопроса и вариантов ответа
let variants = "";
let answer = ""; // для хранения ответа от сервера ('left' или 'right')
let start = "start"; // для отправки на сервер, чтобы сервер выкинул вопрос и варианты ответа
let stat = true; // для работы после воспроизведения видео
let procent = ""; // для хранения значения процента
let fact = ""; // для хранения интересного факта
// для определения прихода процента и факта
let ch1 = 0;
let diside = 0;

const runWebSocket = () => {
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
    // проверка на вопроc
    if (event.data[0] === "Q"){ 
      question = event.data.slice(1);
      if (stat === true){
        console.log(question);
      }
    }
    // проверка на варианты ответов
    if (event.data[0] === "V"){ 
      variants = event.data.slice(1).split("  ");
      if (stat === true){
        console.log(variants);
        $("#question").text(question);
        $("#answer-left").text(`${variants[0]}`);
        $("#answer-right").text(`${variants[1]}`);
        // clearInterval(intervalId);
        // setTimeout(() => {intervaltime();}, 2000);
        // socket.send("2000")
      }
    }
    // проверка на ответ от сервера ('left' или 'right')
    else if(event.data[0] === "A"){
      answer = event.data;
      console.log(answer);
      socket.send(start)
    }
  // проверка на процент
    else if(event.data[0] === "P"){
      ch1 = 1;
      console.log('ch1 = 1');
      procent = event.data.slice(1);
    }
    // проверка на факт
    else if(ch1 === 1 && event.data[0] === "F"){
      $("#fact").text(`Интересный факт: ${event.data.slice(1)}`);
      $("#procent").text(`${procent} людей ответило также`);
      }
    else if(event.data === 'Break'){
      endWorkout();
      $("#question").text("Спасибо, вы ответили на все заданные вам вопросы");
      $("#fact").text("");
      $("#procent").text("");
      $("#answer-left").text("");
      $("#answer-right").text("");
    }
      // проверка на ошибку при обнаружении лица
    else if(event.data[0] === 'E'){
      console.log(event.data);
    }
  });
  
  // Listen for errors
  socket.onerror = function(error) {
    console.log('Websocket error: ', error.message);
  };
  
  socket.onopen = () => {
    console.log(`Connected to ${url}`);
    startWorkout();
  }
};

const intervaltime = () => {
  intervalId = setInterval(() => {
    if (stat === false){
      stat = true;
    }
    socket.send(getFrame());
  }, 1000 / FPS);
};

const startWorkout = () => {
  console.log('start workout clicked!');
  console.log(start)
  socket.send(start); // отправка start для вывода первого вопроса
  intervaltime();
};
