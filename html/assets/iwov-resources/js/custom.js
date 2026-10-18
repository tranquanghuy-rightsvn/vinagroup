(function ($) {
  if (!$) return;

  $(function () {
    var $carousel = $('#carouselExampleIndicators');
    if (!$carousel.length) return;

    var $items = $carousel.find('.carousel-item');
    var total = $items.length;
    if (!total) return;

    $carousel.on('click', '.carousel-control-prev, .carousel-control-next', function (e) {
      e.preventDefault();
      e.stopPropagation();

      var isNext = $(this).hasClass('carousel-control-next');
      var currentIndex = $items.filter('.active').index();
      var nextIndex = (currentIndex + (isNext ? 1 : -1) + total) % total;

      $carousel.carousel(nextIndex);
    });
  });
})(window.jQuery);
