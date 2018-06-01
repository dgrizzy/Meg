// Define title for manipulation
var title = document.body.getElementsByTagName("h1")[0]

// Function for Change to Black
var makeBlack = function() {
  title.style.color = "Black";
}


//Add Event to Change it to Blue
document.getElementById("changeBlue").addEventListener("click", function() {
  title.style.color = "Blue";
  document.getElementById("changeBlue").addEventListener("click", makeBlack);
});

//Add Event to Change it to Red
document.getElementById("changeRed").addEventListener("click", function() {
  title.style.color = "Red";
});

//________TO DO LIST APP________


var goButton = document.getElementById('goButton');

var ourList = document.getElementById("theList");

var finishTask = function() {
  this.parentNode.removeChild(this)
}



var addNewTask = function() {
  //grab text
  var inputBoxValue = document.getElementById('newTask').value;

  //create element
  var newLI = document.createElement("li");

  //create inner element
  var innerButton = document.createElement('button');

  innerButton.innerText = inputBoxValue;

  newLI.id = inputBoxValue;

  newLI.appendChild(innerButton);

  ourList.appendChild(newLI);
  // Other functionality: add the event listener for removal.

  document.getElementById(inputBoxValue).addEventListener("click", finishTask)

  if (inputBoxValue in document.getElementsByI('theList')
}


var makeTitleRed = function() {
  document.getElementsByTagName("h1")[0].style.color = "Red"
}

// Use Button to Provide an Event
goButton.addEventListener("click", addNewTask);

// add on-enter
document.getElementById('newTask').addEventListener("keyup", function(event) {
  if (event.keyCode == 13){
    addNewTask();
  }
});
