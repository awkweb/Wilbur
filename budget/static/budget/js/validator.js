$("#transaction-add-submit").click(function(event) {
    event.preventDefault();

    var form = $('#transaction-add');

    $.ajax({
        url: form.attr('action'),
        type: form.attr('method'),
        data: form.serialize(),
        success: function (data) {
            console.log(data)
            if (!(data['success'])) {
                // Here we replace the form, for the
                form.replaceWith(data['form_html']);
            }
            else {
                // Here you can show the user a success message or do whatever you need
                var next = form.attr('next');
                window.location.replace(next);
                //form.find('.success-message').show();
            }
        },
        error: function () {
            form.find('.error-message').show()
        }
    });
});