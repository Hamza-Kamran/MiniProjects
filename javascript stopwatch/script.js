var Interval; 
function Start() {
    Interval = setInterval(IncrementTens, 10); 
}

function Reset() {
  var seconds = "00"; 
  var tens = "00"; 
  document.getElementById('Seconds').innerHTML = seconds; 
  document.getElementById('Tens').innerHTML = tens; 
}

function IncrementTens() {
  var millis = document.getElementById('Tens').innerHTML; 
  millis = parseInt(millis)+1;
  if (millis < 9){
    document.getElementById('Tens').innerHTML = "0" + millis;
  }
  else if (millis < 99) {
    document.getElementById('Tens').innerHTML = millis.toString();
  }
  else {
    var seconds = document.getElementById('Seconds').innerHTML; 
    seconds = parseInt(seconds); 
    document.getElementById('Seconds').innerHTML = (seconds+1).toString();
    
    document.getElementById('Tens').innerHTML = "00";
  }
  
}

function Stop() {
  clearInterval(Interval); 
}