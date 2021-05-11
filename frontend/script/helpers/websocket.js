const url = 'ws://localhost:5000';

const socket = new WebSocket(url);

questions_vars = ""; // для хранения вопроса и вариантов ответа
answer = ""; // для хранения ответа от сервера ('left' или 'right')
start = "start"; // для отправки на сервер, чтобы сервер выкинул вопрос и варианты ответа

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
    // проверка на вопрос с вариантами
    if (event.data[0] === "Q"){ 
      questions_vars = event.data;
      console.log(questions_vars);
      setTimeout(() => {console.log("TimeOut");}, 2000);    //   !!! Don't working !!!
    }
    // проверка на ответ от сервера ('left' или 'right')
    else if(event.data[0] === "A"){
      answer = event.data;
      console.log(answer);
      socket.send(start);
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
  intervalId = setInterval(() => {
    socket.send(getFrame());
  }, 1000 / FPS);
};
