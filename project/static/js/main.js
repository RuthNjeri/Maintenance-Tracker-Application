
window.onload = function() {
    //create text for the footer
    var year = new Date().getFullYear();
    text = "Developed by Ruth Waiganjo "+"© " + year + " Nairobi"
    document.getElementById("date-footer").innerHTML = text;



// User sign up
let reg = document.getElementById('addUser')
if (reg){
    reg.addEventListener
    ('submit', addUser);
}

function addUser(e){
    e.preventDefault();

    let email = document.getElementById('email').value;
    let first_name = document.getElementById('first_name').value;
    let last_name = document.getElementById('last_name').value;
    let password = document.getElementById('password').value;
    let confirm_password = document.getElementById('confirm_password').value;

    fetch('http://127.0.0.1:5000/api/v2/auth/signup', {
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-type':'application/json'
        },
        body:JSON.stringify({email:email, first_name:first_name, last_name:last_name,
            password:password, confirm_password:confirm_password})
        })
        .then((res) => res.json())
        .then((data) => {
            if (data.response != undefined){
                document.getElementById('output').innerHTML = data.response
            }
            if (data.successful && data.successful === true){
                window.location = data.redirect_url
            }
        })

    }

// User Login

let signin = document.getElementById('login')
if (signin){
    signin.addEventListener
    ('submit', login);
    function login(e){
    e.preventDefault();

    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;

    fetch('http://127.0.0.1:5000/api/v2/auth/login', {
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-type':'application/json'
        },
        body:JSON.stringify({email:email,password:password,})
        })
        .then((res) => res.json())
        .then((data) => {
            if (data.response != undefined){
                document.getElementById('output').innerHTML = data.response
            }
            // store the token created when user is logged in
            window.localStorage.setItem('token', data.token);
        })

    }


}

// window onload curlybrace
}








