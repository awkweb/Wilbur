(function() {
  $(document).ready(function() {
    $('.message').append('<span class="message-close">&times;</span>');
    $('.message-close').on('click', function() {
      $(this).closest('.message').fadeOut();
    });
  });

}).call(this);
