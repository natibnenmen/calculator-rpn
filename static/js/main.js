//const requestType = non;

function clearDisplay() {
    document.getElementById("display").value = '';
}

function appendToken(token) {
    document.getElementById("display").value += token
}

function setRequestType(){
    btn = document.getElementById("rt");
    var color = btn.style.color;
    if(color == "red") {
        btn.style.color = "green";
    }
    if(color == "green") {
        btn.style.color = "red";
    }
}

function calculateResult() {
    req = new XMLHttpRequest();
    var restype = '';
    
    if(document.getElementById("rt").style.color == 'green'){
        var restype = '&restype=color'
    }
    
    const url = "http://localhost:5000/calculate?expression=" + document.getElementById('display').value.replace('+', 'a').replace('^', 'b') + restype;

    var xhttp = new XMLHttpRequest();

    xhttp.open("GET", url, true);
    console.log('url', url);
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('data', data)
            display.style.color = data.color;
            display.value = data.result;                        
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            display.value = 'Error';
        })
}

function getOperators(){

    req = new XMLHttpRequest();

    const url = `http://localhost:5000/operations`;

    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", url, true);

    console.log('url', url);
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('data', data);
            console.log('data.result', data.result);
            btn = document.getElementById("btn");
            for (ix in data.result){
                i = data.result[ix];
                console.log('i:', i);
                node = document.createElement('button');
                node.innerHTML = "<button onclick=appendToken('" + i.toString() + "')>" + i.toString() +"</button>"
                btn.appendChild(node);
                node = null;
            }
            console.log('2. btn', btn)
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            display.value = 'Error';
        })
    setColor();
}

function setColor() {
    document.getElementById("rt").style.color = "red";
    
}