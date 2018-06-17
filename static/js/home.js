$(document).ready(function(){
  $('.ui.dropdown').dropdown();
  $('.special.cards .image').dimmer({
  on: 'hover'
  });
});

var change = document.getElementById('editbtn');
var save = document.getElementById('savebtn');
var hideShow = document.getElementById('showDiv');

change.addEventListener('click', changeText, true);
// save.addEventListener('click', editableTextBlurred, true);

function changeText(){
  var oldText = $(this).prev('div').html();

  var editableText = $("<textarea cols='130', rows='5' />");
  editableText.val(oldText);
  $(this).prev('div').replaceWith(editableText);
  editableText.focus();
  editableText.blur(editableTextBlurred);
  change.classList.add('hideload');
  hideShow.classList.remove('hideload');
}


function editableTextBlurred() {
    var html = $(this).val();
    var a = $('textarea').val();
    var viewableText = $("<div>");
    viewableText.html(html);
    $(this).replaceWith(viewableText);
    // setup the click event for this new div
    viewableText.click(changeText);
    change.classList.remove('hideload');
    hideShow.classList.add('hideload');
    save.classList.remove('hideload');
}
