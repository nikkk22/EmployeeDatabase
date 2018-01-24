$(function () {
    $('#form_validation').validate({
        rules: {
            'checkbox': {
                required: true
            },
            'gender': {
                required: true
            }
        },
        highlight: function (input) {
            $(input).parents('.form-line').addClass('error');
        },
        unhighlight: function (input) {
            $(input).parents('.form-line').removeClass('error');
        },
        errorPlacement: function (error, element) {
            $(element).parents('.form-group').append(error);
        },
		 submitHandler: function(form) {
			// call your function
			var empData = {
				fName:$('#fName').val(),
				mName:$('#mName').val(),
				lName:$('#lName').val(),
				email:$('#email').val(),
				contactNumber:$('#contactNumber').val(),
				manager:$('#manager').val(),
				description:$('#description').val(),
				
			}
			alert(JSON.stringify(data));
			
			$.ajax({
				url: 'localhost:52557/AddEmp',
				type: 'post',
				dataType: 'json',
				success: function (data) {
					alert('Data Saved');
				},
				data: empData
			});
		}
		
    });
});