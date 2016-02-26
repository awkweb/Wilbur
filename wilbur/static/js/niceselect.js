
/*  jQuery Nice Select - v1.0
    http://hernansartorio.github.io/jquery-nice-select
    Made by Hernán Sartorio
 */

(function() {
  (function($) {
    $.fn.niceSelect = function() {
      this.each(function() {
        var dropdown, options, select, selected;
        select = $(this);
        if (!select.next().hasClass('nice-select')) {
          select.after('<div class="nice-select ' + (select.attr('class') || '') + (select.attr('disabled') ? 'disabled' : '" tabindex="0') + '"><span class="current"></span><ul class="list"></ul></div>');
          dropdown = select.next();
          options = select.find('option');
          selected = select.find('option:selected');
          dropdown.find('.current').html(selected.data('display') || selected.text());
          options.each(function() {
            var display;
            display = $(this).data('display');
            dropdown.find('ul').append('<li class="option ' + ($(this).is(':selected') ? 'selected' : '') + '" data-value="' + $(this).val() + (display ? '" data-display="' + display : '') + '">' + $(this).text() + '</li>');
          });
          select.hide();
        }
      });

      /* Event listeners */
      $(document).off('.nice_select');
      $(document).on('click.nice_select', '.nice-select', function(event) {
        var dropdown;
        dropdown = $(this);
        $('.nice-select').not(dropdown).removeClass('open');
        dropdown.toggleClass('open');
        if (dropdown.hasClass('open')) {
          dropdown.find('.option');
          dropdown.find('.focus').removeClass('focus');
          dropdown.find('.selected').addClass('focus');
        } else {
          dropdown.focus();
        }
      });
      $(document).on('click.nice_select', function(event) {
        if ($(event.target).closest('.nice-select').length === 0) {
          $('.nice-select').removeClass('open').find('.option');
        }
      });
      $(document).on('click.nice_select', '.nice-select .option', function(event) {
        var dropdown, option, text;
        option = $(this);
        dropdown = option.closest('.nice-select');
        dropdown.find('.selected').removeClass('selected');
        option.addClass('selected');
        dropdown.find('.focus').removeClass('focus');
        dropdown.find('.selected').addClass('focus');
        text = option.data('display') || option.text();
        dropdown.find('.current').text(text);
        dropdown.prev('select').val(option.data('value')).trigger('change');
      });
      $(document).on('keydown.nice_select', '.nice-select', function(event) {
        var dropdown, focused_option;
        dropdown = $(this);
        focused_option = $(dropdown.find('.focus') || dropdown.find('.list .option.selected'));
        if (event.keyCode === 32 || event.keyCode === 13) {
          if (dropdown.hasClass('open')) {
            focused_option.trigger('click');
          } else {
            dropdown.trigger('click');
          }
          return false;
        } else if (event.keyCode === 40) {
          if (!dropdown.hasClass('open')) {
            dropdown.trigger('click');
          } else {
            if (focused_option.next().length > 0) {
              dropdown.find('.focus').removeClass('focus');
              focused_option.next().addClass('focus');
            }
          }
          return false;
        } else if (event.keyCode === 38) {
          if (!dropdown.hasClass('open')) {
            dropdown.trigger('click');
          } else {
            if (focused_option.prev().length > 0) {
              dropdown.find('.focus').removeClass('focus');
              focused_option.prev().addClass('focus');
            }
          }
          return false;
        } else if (event.keyCode === 27) {
          if (dropdown.hasClass('open')) {
            dropdown.trigger('click');
          }
        } else if (event.keyCode === 9) {
          if (dropdown.hasClass('open')) {
            return false;
          }
        }
      });
    };
  })(jQuery);

}).call(this);
