$(function () {
    $('#employee_search').validate({
        rules: {
            email: {
                required: true,
                minlength: 3
            }
        },
        highlight: function (input) {
            console.log(input);
            $(input).parents('.form-line').addClass('error');
        },
        unhighlight: function (input) {
            $(input).parents('.form-line').removeClass('error');
        },
        errorPlacement: function (error, element) {
            $(element).parents('.input-group').append(error);
        },
        submitHandler: function (form, event) {
		    event.preventDefault();
			var emailId = $('#email').val();
			console.log('Searching for email: ' + emailId);	
			searchEmployee(emailId);
        }
    });
	
	function searchEmployee(emailId)
	{
		$.ajax({
			url: 'http://localhost:52557/SearchEmployee?email=' + emailId,
			type: 'get',
			success: function (data) {
				console.log('Success' + data);
				//Clear Table
				$("#empTable").empty();
				data = data.replace(/'/g,'"');
				data = JSON.parse(data);
				if(data.length==0)
					alert('No match found');
				//else if(data.length==1)		
				//{
					//Fill Record details 
					
					//show popup with emp details
				//	$('#empDetail').modal('show'); 	
				//}
				else
				{
					//Fill Table
					var names = Object.keys(data[0]);

					//Table Header
					var tbl_header = document.createElement("thead");
					var tbl_hed_row = tbl_header.insertRow();
					$.each(names, function (k, v) {
						var cell = tbl_hed_row.insertCell();
						cell.appendChild(document.createTextNode(v.toString()));
					})

					//Table Body
					var tbl_body = document.createElement("tbody");
					$.each(data, function () {
						var tbl_row = tbl_body.insertRow();
						var emailId = this.Email;
						$(tbl_row).css( 'cursor', 'pointer' );
						$(tbl_row).attr('title', 'click to see detail');
						$(tbl_row).click({emailId: this.Email}, reSearchEmployee);						
						function reSearchEmployee(event){
							//alert(event.data.emailId);
							searchEmployee(event.data.emailId);
						}
						$.each(this, function (k, v) {
							var cell = tbl_row.insertCell();
							var cellVal = (v == null) ? "" : v;
							cell.appendChild(document.createTextNode(cellVal.toString()));
						})
					})
					
					//Clear Table
					$("#empTable").empty();
					//Add Table Header
					$("#empTable").append(tbl_header);
					//Add Table Body
					$("#empTable").append(tbl_body);
				}
			},
			error: function (data) {
				alert('Error:' + data);
			}
		});	
	}
});