var questionNum = document.getElementById("question").innerText.slice(1,);
questionNum = questionNum.replace(':', '');
questionNum = parseInt(questionNum, 10);

if(questionNum % 7 == 0) {
  var countDownTimer = 7;
  ChangeTimerColor();
} else
  var countDownTimer = 30;
document.getElementById("timer").innerHTML = countDownTimer;
var answers = document.getElementById("answers").getElementsByTagName("p");
console.log(answers);
var max = 0;
for(var i = 0; i < answers.length; i++) {
  max = Math.max(max, answers[i].innerHTML.length);
}

for(var i = 0; i < answers.length; i++) {
  answers[i].getElementsByTagName("input")[0].style.width = (max * 5).toString() + "px";
  answers[i].getElementsByTagName("input")[0].style.border = "0";
  //answers[i].getElementsByTagName("input")[0].style.padding = "9px 20px";
  answers[i].getElementsByTagName("input")[0].style.margin = "4px 0px";
  answers[i].getElementsByTagName("input")[0].style.transitionDuration='0.4s';
};

// Update the count down every 1 second
var x = setInterval(function() {
  countDownTimer -= 1;
  if(countDownTimer <= 7)
    ChangeTimerColor();  
  document.getElementById("timer").innerHTML = countDownTimer;
  if (countDownTimer < 0) {
    clearInterval(x);
    document.getElementById("timer").innerHTML = "Time's UP!";
    setTimeout(function () {
      document.getElementById("answers").submit();
    }, 1250);
  }
}, 1250);

function ChangeTimerColor() {
  document.getElementById("timer").style.color = "#dd2e44";
  document.getElementById("timer").style.transitionDuration= "1s";
}