(function() {
  $('.meter-animate').each(function() {
    var width;
    width = $(this).data('width');
    $(this).animate({
      width: width
    });
  });

}).call(this);
