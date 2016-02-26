(function() {
  var select;

  select = $('#selectdate');

  select.change(function() {
    var month, option, value, year;
    option = $('#selectdate option:selected');
    value = option.val();
    year = option.data('year');
    month = option.data('month');
    $.ajaxSetup({
      headers: {
        'X-CSRFToken': Cookies.get('csrftoken')
      }
    });
    $.ajax({
      url: window.location.pathname,
      type: 'post',
      data: {
        'selectdate_value': value,
        'year': year,
        'month': month
      },
      success: function(data) {
        var html;
        if (data['success']) {
          html = $('#content-ajax');
          html.replaceWith(data['html']);
        }
      },
      error: function() {
        form.find('.error-message').show();
      }
    });
  });

}).call(this);
