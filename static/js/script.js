$(document).ready(function(){
  $('.ui.dropdown').dropdown();
});

var faculty = document.getElementById('faculty');

faculty.addEventListener('click', function(){
  modifyText();
});

faculty.addEventListener('change', function(){
  modifyText();
});



function modifyText(){
  var fl = $('#faculty').val();
  $.getJSON(
    data = '/options/' + fl,
    function(data){
      // Remave old options
      $('#department').find('option').remove();
      var option1 = '<option>Department</option>';
      $('#department').append(option1);
      // Add new items
      $.each(data, function(key, val){
        for (var i = 0; i < val.length; i++) {
          var option = '<option value="' + val[i][0] + '">' + val[i][1] + '</option>'
          $('#department').append(option);
        }
      });
    });
}
