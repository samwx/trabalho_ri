jQuery(document).ready(function($) {

  $('#filterResults').change(function(){
  	console.log($(this).val());
  	if ($(this).val() == 'positive') {
	  	$('.positive').fadeIn();
	  	$('.negative').fadeOut();
  	}

  	if ($(this).val() == 'negative') {
  		$('.negative').fadeIn();
	  	$('.positive').fadeOut();
  	}

  	if ($(this).val() == '') {
  		$('.negative').fadeIn();
  		$('.positive').fadeIn();
  	}
  });
});
