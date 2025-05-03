let btnSignUp = document.querySelector("#sign-up")

btnSignUp.addEventListener("click", (event) => {
  console.log("Click")
    registroUsuario();
});

async function registroUsuario() {
  response = await fetch('http://localhost:8000/', {
    method: 'POST',
    headers: {
      'accept': 'application/json',
      'Content-Type': 'application/json'
    },
    // body: '{\n  "username": "malamixi",\n  "password": "mala1"\n}',
    body: JSON.stringify({
      'username': valorInputUsername,
      'password': valorInputPassword
    })
  });
  console.log(response.data)
  return response.data
  
}

function isUserLogged(){
  const token = localStorage.getItem("token");
  if(token == ""){
    return false
  } else {
    return true
  }
}

async function getTokenFromLogin() {
  response = await fetch('http://localhost:8000/login', {
    method: 'POST',
    headers: {
      'accept': 'application/json',
      'Content-Type': 'application/json'
    },
    // body: '{\n  "username": "malamixi",\n  "password": "mala1"\n}',
    body: JSON.stringify({
      'username': valorInputUsername,
      'password': valorInputPassword
    })
  });
  console.log(response.data)
  localStorage.setItem("token", response.data.access_token);

  return response.data
}

async function verLibros() {
  const token = localStorage.getItem("token");
  url = `http://localhost:8000/books?token=${token}`
  response = await fetch(url, {
    method: 'GET',
    headers: {
      'accept': 'application/json',
      'Content-Type': 'application/json'
    },
  });
  console.log(response)
  console.log(response.data)
  return response
}

async function verPrestamos() {
  const token = localStorage.getItem("token");
  url = `http://localhost:8000/prestamos?token=${token}`
  response = await fetch(url, {
    method: 'GET',
    headers: {
      'accept': 'application/json',
      'Content-Type': 'application/json'
    },
  });
  console.log(response)
  console.log(response.data)
  return response
}

async function verUsuarios() {
  const token = localStorage.getItem("token");
  url = `http://localhost:8000/users?token=${token}`
  response = await fetch(url, {
    method: 'GET',
    headers: {
      'accept': 'application/json',
      'Content-Type': 'application/json'
    },
  });
  console.log(response)
  console.log(response.data)
  return response
}