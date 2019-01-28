
window.onload = function() {
  var timerInput = document.getElementById('timer').getElementsByTagName('input')[0];
  var startStop = document.getElementById('button-start-stop');
  var reset = document.getElementById('button-reset');
  var t;
  var seconds = timerInput.value;

  function decrease() {
    seconds--;
    timerInput.value = seconds;
  }
  function startTimer() {
    t = setInterval(decrease, 1000);
    startStop.value = "Stop";
  }
  function stopTimer() {
    clearInterval(t)
    startStop.value = "Start";
  }
  function resetTimer() {
    stopTimer();
    seconds = 600;
    timerInput.value = seconds;
  }
  reset.onclick = resetTimer;

  startStop.onclick = function() {
    if (startStop.value == "Start") {
      t = setInterval(decrease, 1000);
      startStop.value = "Stop";
    } else if (startStop.value == "Stop") {
      clearInterval(t)
      startStop.value = "Start";
    }
  }

}
