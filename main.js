(function($) {
  // Returns a function, that, as long as it continues to be invoked, will not
  // be triggered. The function will be called after it stops being called for
  // N milliseconds. If `immediate` is passed, trigger the function on the
  // leading edge, instead of the trailing.
  function debounce(func, wait, immediate) {
    var timeout;
    return function() {
      var context = this, args = arguments;
      var later = function() {
        timeout = null;
        if (!immediate) func.apply(context, args);
      };
      var callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (callNow) func.apply(context, args);
    };
  }; 
  
  function uuid4() {
    // generate uuid http://stackoverflow.com/a/2117523/4032871
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {var r = Math.random()*16|0,v=c=='x'?r:r&0x3|0x8;return v.toString(16);});
  }

  var state = {};

  var client_id = localStorage.getItem('client_id');
  if (client_id === null) {
    client_id = uuid4();
    localStorage.setItem('client_id', client_id);
  }

  var rsvp_id = uuid4();
  var reqQueue = $.Deferred().resolve();

  function save_form($form, addition) {
    var req_body = {
      'rsvp': $form.find('[name=rsvp]').val() === 'yes',
      'email': $form.find('[name=email]').val(),
      'details': $form.find('[name=details]').val(),
    };
    if (addition !== undefined) {
      $.extend(req_body, addition);
    }
    var args = {
      url: '/api/rsvp/' + rsvp_id,
      method: 'PUT',
      data: JSON.stringify(req_body),
      dataType: 'json',
      headers: {
        'X-Heidtco-Client-Id': client_id,
        'Content-type': 'application/json',
      }
    };
    reqQueue = reqQueue.done(function() {
      return $.ajax(args);
    });
    return reqQueue;  
  }


  $(document).on('click', '.rsvp-yes', function(ev) { $('.rsvp .buttons').hide(); $('form.yes').show(); });
  $(document).on('click', '.rsvp-regrets',  function(ev) { $('.rsvp .buttons').hide(); $('form.regrets').show(); });

  $(document).on('change keydown', 'form[ajax-rsvp]', debounce(function(ev) {
    save_form($(this), { status: 'in-progress' }).done(function(data, textStatus, jqXHR) {
      // nothing to do
      console.log('saved rsvp in progress', rsvp_id);
    });
  }, 3000));

  $(document).on('submit', 'form[ajax-rsvp]', function(ev) {
    ev.preventDefault();
    var $form = $(this);
    save_form($form, { status: 'complete' }).done(function(data, textStatus, jqXHR) {
      console.log('saved rsvp complete', rsvp_id);
    });
    // generate new id so any further work goes to another rsvp object
    rsvp_id = uuid4();
    $form.addClass('done').one('transitionend', function() {
      $form.next('.thanks').addClass('show');
    });
  });

})(jQuery);
