/**
 * Created with PyCharm.
 * User: keyvan
 * Date: 9/16/13
 * Time: 3:57 PM
 * To change this template use File | Settings | File Templates.
 */

//var url = window.location;
//// Will only work if string in href matches with location
//$('ul.nav a[href="'+ url +'"]').parent().addClass('active');
//
//// Will also work for relative and absolute hrefs
//$('ul.nav a').filter(function() {
//    return this.href == url;
//}).parent().addClass('active');


function validate_number(evt) {
    var e = evt || window.event;
    var key = e.keyCode || e.which;

    if (!e.shiftKey && !e.altKey && !e.ctrlKey &&
    // numbers
    key >= 48 && key <= 57 ||
    // Numeric keypad
    key >= 96 && key <= 105 ||
    // Backspace and Tab and Enter
    key == 8 || key == 9 || key == 13 ||
    // Home and End
    key == 35 || key == 36 ||
    // left and right arrows
    key == 37 || key == 39 ||
    // Del and Ins
    key == 46 || key == 45) {
        // input is VALID
    }
    else {
        // input is INVALID
        e.returnValue = false;
        if (e.preventDefault) e.preventDefault();
    }
}

function show_all_links_click() {
    if(document.getElementById('all_links').checked)
        $('#id_number_of_linkages_to_show').attr("disabled", "disabled");
    else
        $('#id_number_of_linkages_to_show').removeAttr('disabled');
}

function language_changed() {
    if($('#id_language').val() != 'en')
    {
        $('#relex_simple').attr("disabled", "disabled");
        $('#relex_opencog').attr("disabled", "disabled");

        $('#relex_simple').removeAttr("checked")
        $('#relex_opencog').removeAttr("checked")
    }
    else
    {
        $('#relex_simple').removeAttr('disabled');
        $('#relex_opencog').removeAttr('disabled');
    }
}