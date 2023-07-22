const colors = ["red", "orange", "yellow", "green", "light blue", "blue", "violet"]; 
console.log(1); 
const btn = document.getElementById("color-btn"); 


btn.addEventListener("click", function() {

	var randomNum = Math.floor(Math.random() * colors.length); 
	document.body.style.backgroundColor = colors[randomNum]; 

}); 
