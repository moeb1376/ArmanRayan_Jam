let globalFormID = 2;
function onSubmit(token) {
    document.getElementById(globalFormID).submit();
}

function validate(event) {
    event.preventDefault();
    grecaptcha.execute();

}

function recaptcha_onload(elementID,formID) {
    var element = document.getElementById(elementID);
    globalFormID = formID;
    element.onclick = validate;
}