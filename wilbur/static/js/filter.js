// Generated by CoffeeScript 1.10.0
(function() {
  var select;

  select = $('#filter');

  select.change(function() {
    var month, option, select_value, year;
    option = $('#filter option:selected');
    select_value = option.val();
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
        'action': 'selectdate',
        'select_value': select_value,
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

//# sourceMappingURL=filter.js.map
