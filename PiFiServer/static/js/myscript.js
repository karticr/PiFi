$(document).ready( function(){
    $('#auto').load('/yolo');
    refresh();
    });
     
    function refresh()
    {
        setTimeout( function() {
          $('#auto').fadeOut('slow').load('/yolo').fadeIn('slow');
          refresh();
        }, 2000);
    }