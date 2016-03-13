(function() {
  $('.meter-animate').each(function() {
    var width;
    width = $(this).data('width');
    width = width > 100 ? 100 : width;
    $(this).animate({
      width: width + "%"
    });
  });

}).call(this);
