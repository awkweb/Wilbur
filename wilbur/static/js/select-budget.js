(function() {
  $.fn.selectFilter = function() {
    var select;
    select = $(this);
    return select.change(function() {
      var link, option;
      option = select.find(":selected");
      link = option.data('link');
      return location.href = link;
    });
  };

}).call(this);
