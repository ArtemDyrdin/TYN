const url = 'ws://localhost:5000';

const socket = new WebSocket(url);

question = ""; // для хранения вопроса и вариантов ответа
variants = "";
answer = ""; // для хранения ответа от сервера ('left' или 'right')
start = "start"; // для отправки на сервер, чтобы сервер выкинул вопрос и варианты ответа
stat = false; // для работы после воспроизведения видео
procent = ""; // для хранения значения процента
fact = ""; // для хранения интересного факта
// для определения прихода процента и факта
ch1 = 0;

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
        $("#question_fact").text(question);
        setTimeout(() => {console.log("TimeOut");}, 2000);
      }
    }
    // проверка на варианты ответов
    if (event.data[0] === "V"){ 
      variants = event.data.slice(1).split("  ");
      if (stat === true){
        console.log(variants);
        $("#variants_procent").text(`${variants[0]}  ${variants[1]}`);
        clearTimeout(intervalId);
        setTimeout(() => {
          intervalId = setInterval(() => {
            socket.send(getFrame());
          }, 1000 / FPS);
        }, 2000);
      }
    }
    // проверка на ответ от сервера ('left' или 'right')
    else if(event.data[0] === "A"){
      answer = event.data;
      console.log(answer);
      socket.send(start);
    }
    // проверка на процент
    else if(event.data[0] === "P"){
      ch1 = 1;
      console.log('ch1 = 1')
      procent = event.data.slice(1);
    }
    // // проверка на факт
    else if(ch1 === 1 && event.data[0] === "F"){
      $("#question_fact").text(event.data.slice(1));
      $("#variants_procent").text(procent);
      endWorkout();                                       // НЕ ОСТАНАВЛИВАЕТСЯ
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

const startWorkout = () => {
  console.log('start workout clicked!');
  console.log(start)
  socket.send(start); // отправка start для вывода первого вопроса
  $("#question_fact").text("Чтобы начать разрешите съемку и наклоните голову в лево или право");
  intervalId = setInterval(() => {
    if (stat === false){
      stat = true;
    }
    socket.send(getFrame());
  }, 1000 / FPS);
};
