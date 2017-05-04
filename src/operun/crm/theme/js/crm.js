(function($) {
  "use strict"; // Start of use strict

  $(document).ready(function() {
    $('.template-contact #form-widgets-title').change(function() {
      var field = $(this).val().split(' ');
      if ($('.template-contact #form-widgets-firstname').val() == '') {
        $('.template-contact #form-widgets-firstname').val(field[0]);
      };
      if ($('.template-contact #form-widgets-lastname').val() == '') {
        $('.template-contact #form-widgets-lastname').val(field[1]);
      };
    });
  });

})(jQuery); // End of use strict
