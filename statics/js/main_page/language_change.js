function delete_matlab() {
    competition = document.getElementById('id_competition');
    console.log(competition);
    language_option = document.getElementById("id_language").options[3];
    console.log(language_option);
    console.log(competition.options.length);
    console.log(competition[competition.selectedIndex].value);

    // mentor_input = document.getElementById('id_mentor').parentNode;
    if (competition.options.length > 0) {
        language_option.hidden = competition[competition.selectedIndex].value < 3;
        // mentor_input.hidden = competition[competition.selectedIndex].value >= 3;
    }
}
function delete_matlab_jquery() {
    let matlab = $("span:contains('Matlab')").parent();
    let competition = $("#id_competition");
    matlab.attr('hidden',competition[0].selectedIndex<3);
}