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
				gender:$('input[name=gender]:checked').val(),
			}
			alert(JSON.stringify(empData));
			
			$.ajax({
				url: 'http://localhost:52557/AddEmp',
				type: 'get',
				//dataType: 'json',
				success: function (data) {					
				$('#fName').val('');
				$('#mName').val('');
				$('#lName').val('');
				$('#email').val('');
				$('#contactNumber').val('');
				$('#manager').val('');
				$('#description').val('');
				$('#checkbox').prop('checked', false);
					alert('Success' + data);
				},
				error: function (data) {
					alert('Error:' + data);
				},
				data: empData
			});
		}
		
    });
});
