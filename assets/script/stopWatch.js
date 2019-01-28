
window.onload = function() {
  var timerInput = document.getElementById('timer').getElementsByTagName('input')[0];
  var startStop = document.getElementById('button-start-stop');
  var reset = document.getElementById('button-reset');
  var t;
  var seconds = timerInput.value;

  

  function decrease() {
    if (seconds > 0) {
      seconds--;
      timerInput.value = seconds;
      document.getElementById('form').submit();
    }
  }
  function startTimer() {
    t = setInterval(decrease, 1000);
    startStop.value = "Stop";
  }
  function stopTimer() {
    clearInterval(t)
    startStop.value = "Start";
    document.getElementById('form').submit();
  }
  function resetTimer() {
    stopTimer();
    seconds = 360;
    timerInput.value = seconds;
    document.getElementById('form').submit();
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
