$('.multiple-items').slick({
    dots: false,
    infinite: false,
    nextArrow: '<i class="fa fa-angle-right next" aria-hidden="true"></i>',
    prevArrow: '<i class="fa fa-angle-left prev" aria-hidden="true"></i>',
    speed: 300,
    slidesToShow: 4,
    slidesToScroll: 4,
    responsive: [
        {
            breakpoint: 1024,
            settings: {
                slidesToShow: 3,
                slidesToScroll: 3,
                infinite: true,
                dots: false
            }
        },
        {
            breakpoint: 600,
            settings: {
                slidesToShow: 2,
                slidesToScroll: 2
            }
        },
        {
            breakpoint: 480,
            settings: {
                slidesToShow: 1,
                slidesToScroll: 1
            }
        }
    ]
});