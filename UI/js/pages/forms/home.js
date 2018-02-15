$(function () {
    $('#forgot_password').validate({
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
        submitHandler: function (form) {
            console.log('fetching data');
            // call your function			
            return;

            $.ajax({
                url: 'http://localhost:52557/AddEmp',
                type: 'get',
                //dataType: 'json',
                success: function (data) {
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