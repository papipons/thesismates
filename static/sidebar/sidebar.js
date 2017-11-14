  $('.easy-sidebar-toggle').click(function(e) {
      e.preventDefault();
      $('.easy-sidebar-container').toggleClass('toggled');
      $('.navbar.easy-sidebar').toggleClass('toggled');
  });
  $('html').on('swiperight', function(){
      $('.easy-sidebar-container').addClass('toggled');
      $('.navbar.easy-sidebar').addClass('toggled');
  });
  $('html').on('swipeleft', function(){
      $('.easy-sidebar-container').removeClass('toggled');
      $('.navbar.easy-sidebar').removeClass('toggled');
  });
