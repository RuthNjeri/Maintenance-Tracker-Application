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
            if (data.successful && data.successful === true){

                window.location = "http://127.0.0.1:5000/api/v2/loginredirect/" + data.token

            }
})

}
}
// // User get requests

// function userRequests(e){
//     e.preventDefault();
//     let token = window.localStorage.getItem('token');
//     console.log(token)

//     fetch('http://127.0.0.1:5000/api/v2/users/requests/', {
//         method: 'GET',
//         headers: {
//             'Accept': 'application/json, text/plain, */*',
//             'Content-type':'application/json',
//             'token': token
//         }
//         })
//         .then((res) => res.json())
//         .then((data) => {
//             let output = '<h3>All Requests</h3>';
//             data.forEach(function(users_requests){
//                 output += `
//             <table id="userRequests">
//                 <tr>
//                     <th>ID</th>
//                     <th>Title</th>
//                     <th>Description</th>
//                     <th>Date</th>
//                     <th>Status</th>
//                     <th>Feedback</th>
//                 </tr>
//             </table> 
//                    <td>${users_requests.id}</td>
//                     <td>Computer won't start</td>
//                     <td>When I power up my computer I hear 3 beeps then it shuts down</td>
//                     <td>12/02/94</td>
//                     <td>Resolved</td>
//                     <td>Please bring it to the technicians in 8th floor</td>
//                     <td>edit</td>
//                     <td>delete</td>`;
//             })

//         })

//     }
// window onload curlybrace
}








