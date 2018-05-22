
window.onload = function() {
    //create text for the footer
    var year = new Date().getFullYear();
    text = "Developed by Ruth Waiganjo "+"© " + year + " Nairobi"
    document.getElementById("date-footer").innerHTML = text;

    //validate passwords provided
function comparePassword() {
    var password = document.getElementById("password");
    var confirm_password = document.getElementById("confirm-password");
    if(password.value != confirm_password.value) {
        confirm_password.setCustomValidity("Passwords Don't Match")

    }
    else {
        confirm_password.setCustomValidity('');
    }

    password.onchange = comparePassword;
    confirm_password.onkeyup = comparePassword;
}

}




