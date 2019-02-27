function add_validate_option(element_name, validate = 0) {
    let el = document.getElementsByName(element_name)[0];
    let parent = el.parentElement;
    if (validate !== 0) {
        let temp = validate.split(" ");
        temp.forEach(item => parent.classList.add(item));
    } else {
        el.classList.forEach(item=>parent.classList.add(item));
    }
}