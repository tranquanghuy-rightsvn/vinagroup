$(function(){
	console.log("preloader start");
	var editMode;
	var name = 'isEdit';
	var results = new RegExp('[\?&amp;]' + name + '=([^&amp;#]*)').exec(window.parent.location);
	if (results==null){
		return;
	}else{
		editMode = results[1];
	}
	console.log('isEdit : ' + editMode);
	if(editMode == "true"){
		console.log('inside isEdit true');
		$('body').removeClass('modal-open');
		$("#preloader").removeClass("show").addClass("invisible");
	}else{
		console.log('inside isEdit false');
		$('body').removeClass('modal-open');
		$("#preloader").removeClass("show").addClass("invisible");
	}
	console.log("preloader end");
});