$(function() {
	setTimeout(function(){
		$('.start-up-img').fadeIn(1600);//1600
	},500); 
	setTimeout(function(){
		$('.start-up').fadeOut(500);
	},2500); 
});
// slics
$(document).on('ready', function() {
	$(".full").slick({
		arrows: false,
		dots: true,
		autoplay: false,
		fade: false,
		infinite: false,　　
		pauseOnFocus: false,
		pauseOnHover: false,
		pauseOnDotsHover: false,
	});
  });
  function pushHideButton() {
	var txtPass = document.getElementById("textPassword");
	var btnEye = document.getElementById("buttonEye");
	if (txtPass.type === "text") {
	  txtPass.type = "password";
	  btnEye.className = "fa fa-eye";
	} else {
	  txtPass.type = "text";
	  btnEye.className = "fa fa-eye-slash";
	}
  }

  $('input[name="利用規約"]').change(function() {
	var prop = $('input[name="利用規約"]').prop('checked');
	if (prop) {
	  $('.next').prop('disabled', false);
	  $('.next').addClass('active');
	} else {
	  $('.next').prop('disabled', true);
	  $('.next').removeClass('active');
	}
  });
$('#sms').on("mouseup keyup",function(e){
	var sms = parseInt($(this).val());
    var smsMax = parseInt($(this).attr('max'));
if(sms>smsMax){$(this).val(smsMax);}
});

// serch
$(function(){
	$(function() {
		$(".serch-box,.serch-icon").on('click', function() {
		$(".serch-list-box").slideToggle(500);
		$('.tab-area').slideToggle(500);
		});
	});
  });
  $(function() {
	let tabs = $(".tab"); 
	$(".tab").on("click", function() {
	  $(".open").removeClass("open"); 
	  $(this).addClass("open"); 
	  const index = tabs.index(this); 
	  $(".content").removeClass("show").eq(index).addClass("show"); 
	});
  });
  $(function(){
	$(function() {
		$(".edit").on('click', function() {
		if($('.edit p').text()==='編集'){
			$('.edit p').text('削除');
			$('.fa-chevron-right').css('display','none');
			$('.scales').css('display','block');
		}else{
			$('.edit p').text('編集');
			$('.fa-chevron-right').css('display','block');
			$('.scales').css('display','none');
		}

		});

	});
  });