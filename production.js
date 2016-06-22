(function($) {
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  function sameOrigin(url) {
      // test that a given url is a same-origin URL
      // url could be relative or scheme relative or absolute
      var host = document.location.host; // host + port
      var protocol = document.location.protocol;
      var sr_origin = '//' + host;
      var origin = protocol + sr_origin;
      // Allow absolute or scheme relative URLs to same origin
      return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
          (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
          // or any other URL that isn't scheme relative or absolute i.e relative.
          !(/^(\/\/|http:|https:).*/.test(url));
  }
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
              // Send the token to same-origin, relative URLs only.
              // Send the token only if the method warrants CSRF protection
              // Using the CSRFToken value acquired earlier
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

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
    var $form = $(this);
    if ($form.hasClass('done')) {
      console.log('not saving rsvp in-progress because the form is closed');
      return;
    }
    save_form($form, { status: 'in-progress' }).done(function(data, textStatus, jqXHR) {
      // nothing to do
      console.log('saved rsvp in progress', rsvp_id);
    });
  }, 3000));

  $(document).on('submit', 'form[ajax-rsvp]', function(ev) {
    ev.preventDefault();
    var $form = $(this);
    $form.find('[type=submit]').prop('disabled', true);
    save_form($form, { status: 'complete' }).done(function(data, textStatus, jqXHR) {
      console.log('saved rsvp complete', rsvp_id);
      $form.addClass('done').one('transitionend', function() {
        $form.next('.thanks').addClass('show');
      });
      $form.get(0).scrollIntoView();
    });
    // generate new id so any further work goes to another rsvp object
    rsvp_id = uuid4();
  });

})(jQuery);
