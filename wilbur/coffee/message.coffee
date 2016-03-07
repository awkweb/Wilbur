$(document).ready ->
  $('.message').append '<span class="message-close">&times;</span>'
  $('.message-close').on 'click', ->
    $(this).closest('.message').fadeOut()
    return
  return