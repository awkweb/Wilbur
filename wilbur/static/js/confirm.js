(function() {
  var button;

  button = $('#confirm');

  button.mouseleave(function() {
    var ogText;
    button.removeClass('is-clicked');
    ogText = button.data('original-text');
    button.text(ogText);
  });

  button.mouseenter(function() {
    if (button.hasClass('is-clicked')) {
      button.removeClass('is-clicked');
    }
  });

  button.click(function(e) {
    var altText, link;
    e.preventDefault();
    if (button.hasClass('is-clicked')) {
      link = button.attr('href');
      document.location.href = link;
    } else {
      button.addClass('is-clicked');
      altText = button.data('alt-text');
      button.text(altText);
    }
  });

}).call(this);
