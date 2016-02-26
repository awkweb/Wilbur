(function() {
  var select;

  select = $('#filter');

  select.change(function() {
    var link, option, value;
    option = $('#filter option:selected');
    value = option.val();
    link = value !== '-1' ? "/transactions/budget/" + value + "/" : '/transactions/';
    return window.location.replace(link);
  });

}).call(this);
