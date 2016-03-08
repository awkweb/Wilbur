$('.meter-animate').each ->
  width = $(this).data('width')
  $(this).animate width: width
  return