var scores = document.getElementsByTagName("h3");
if(scores.length > 1) {
    if(scores[0].innerHTML.split(':')[1] > scores[1].innerHTML.split(':')[1])
        var winner = scores[0].innerHTML.split(':')[0];
    else if (scores[0].innerHTML.split(':')[1] < scores[1].innerHTML.split(':')[1])
        var winner = scores[0].innerHTML.split(':')[0];
    else
        var winner = "Tie"


    console.log(scores[0].innerHTML);

    if(winner == "Tie")
        document.getElementsByTagName("h2")[0].innerHTML = "It's a Tie!";
    else
        document.getElementsByTagName("h2")[0].innerHTML = winner + " Wins!";
} else {
    document.getElementsByClassName("score")[0].style.display = "none";
    document.getElementsByTagName("h2")[0].innerHTML = scores[0].innerHTML.split(':')[0] + ", Your Score is: " + scores[0].innerHTML.split(':')[1];
}
