function checkText(){
    const textToType = document.getElementById("textToType").innerText;
    const userInput = document.getElementById("userInput").value;

    if (userInput === textToType) {
      document.getElementById("result").innerText = "Correct!";
      document.getElementById("result").style.color = "green";
    } else {
      document.getElementById("result").innerText = "Try again!";
      document.getElementById("result").style.color = "red";
}}

function alter(){
    
}