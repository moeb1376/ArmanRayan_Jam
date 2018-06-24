function delete_matlab() {
    competition = document.getElementById('id_competition');
    language_option = document.getElementById("id_language").options[3];
    mentor_input = document.getElementById('id_mentor').parentNode;
    if (competition.options.length > 0) {
        language_option.hidden = competition[competition.selectedIndex].value < 3;
        mentor_input.hidden = competition[competition.selectedIndex].value > 3;
    }
}