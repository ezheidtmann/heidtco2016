(function($) {

  $(document).on('click', '.rsvp-yes', function(ev) { $('.rsvp .buttons').hide(); $('form.yes').show(); });
  $(document).on('click', '.rsvp-regrets',  function(ev) { $('.rsvp .buttons').hide(); $('form.regrets').show(); });

})(jQuery);
