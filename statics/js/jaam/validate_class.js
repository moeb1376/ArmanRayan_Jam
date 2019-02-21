function add_validate_option(element_name, validate) {
    let el = document.getElementsByName(element_name)[0];
    let parent = el.parentElement;
    let temp = validate.split(" ");
    temp.forEach(item => parent.classList.add(item));
}