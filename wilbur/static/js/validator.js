(function() {
  $('#form-submit').click(function(e) {
    var form;
    e.preventDefault();
    form = $('#form-grab');
    $.ajaxSetup({
      headers: {
        'X-CSRFToken': Cookies.get('csrftoken')
      }
    });
    $.ajax({
      url: form.attr('action'),
      type: form.attr('method'),
      data: form.serialize(),
      success: function(data) {
        var next;
        if (!data['success']) {
          form.replaceWith(data['form_html']);
        } else {
          next = form.attr('next');
          window.location.replace(next);
        }
      },
      error: function() {
        form.find('.error-message').show();
      }
    });
  });

}).call(this);
