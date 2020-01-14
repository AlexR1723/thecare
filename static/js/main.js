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

$('#send_feedback').click(function () {
    let name = $('#feedback_name')[0].value
    let email = $('#feedback_email')[0].value
    let subject = $('#feedback_subject')[0].value
    let text = $('#feedback_text')[0].value

    // console.log($('#feedback_name').text())

    $.ajax({
        type: "GET",
        dataType: "json",
        async: true,
        url: 'send_feedback',
        data: {
            name: name,
            email: email,
            subject: subject,
            text: text
        },
        success: function (data) {
            if (data == true) {
                // alert('good')
                notice(data,'info','bottomCenter')
            } else {
                // alert('bad')
                // notice(data,'info','bottomCenter')
                notice('false false false false false false false false false false false false false false false ','info','bottomCenter')
            }
        },
        error: function (data) {
            alert('error')
        }
    })
})

function notice(text, type, layout) {
    // function generate(text) {
        new Noty({
            text: text,
            type: type,
            dismissQueue: true,
            layout: layout,
            theme: 'relax'
        }).show();
    // }

    // let el = document.createElement('div')
    // el.setAttribute('class','')
    // el.setAttribute('style','z-index:999;width:30%;height:20%;transform: translate(50%, 50%);')
    //
    // let p = document.createElement('p')
    // p.setAttribute('style','text-align:center')
    //
    // el.appendChild(p)

    // let el = document.getElementById('notice_style')
    // el.innerHTML = text;
    // document.getElementById('notice_style').getBoundingClientRect.top = 90 %
    //     $("#notice_style").fadeIn(1000).delay(2000).fadeOut(1000)


}

// var total_wheel=0;
// window.onwheel= function(e){
//     console.clear()
//     console.log(e.deltaY)
//     total_wheel+=e.deltaY
//     console.log(total_wheel)
//
// }

$('.items-counter').ready(function () {
    $('.minus').click(function () {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) - 1;
        count = count < 1 ? 1 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('.plus').click(function () {
        var $input = $(this).parent().find('input');
        $input.val(parseInt($input.val()) + 1);
        $input.change();
        return false;
    });
});