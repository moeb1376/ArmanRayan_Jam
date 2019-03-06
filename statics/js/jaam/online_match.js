let opponent = 0;

function set_second_team_data(opponent_id, team_data) {
    console.log(team_data);
    console.log(typeof team_data);
    console.log("lighten-5".split(" "));
    opponent = opponent_id;
    let main_card = document.createElement("div");
    "lighten-5".split(" ").forEach(item => main_card.classList.add(item));
    let image = document.createElement("img");
    image.classList.add("center-block");
    image.classList.add("circle");
    image.style.width='50%'
    image.style. padding= '20px';
    image.setAttribute("src", team_data.image);
    main_card.appendChild(image);
    let child_div = document.createElement("div");
    child_div.classList.add("section");
    let team_name_element = document.createElement("h3");
    let team_name_text = document.createTextNode(team_data.team_name);
    team_name_element.appendChild(team_name_text);
    child_div.appendChild(team_name_element);
    let team_university_element = document.createElement("h5");
    let team_university_text = document.createTextNode(team_data.university);
    team_university_element.appendChild(team_university_text);
    child_div.appendChild(team_university_element);
    let team_class_element = document.createElement("h5");
    let team_class_text = document.createTextNode(team_data.class);
    team_class_element.appendChild(team_class_text);
    child_div.appendChild(team_class_element);
    main_card.appendChild(child_div);
    let second_team_element = document.getElementById("second_team");
    let opponent_select = document.getElementById("opponent-select");
    second_team_element.removeChild(opponent_select);
    // second_team_element.childNodes[1].hidden = true;
    second_team_element.appendChild(main_card);


}