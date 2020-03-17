jQuery("document").ready(function ($) {

    var up = $('#block-up');

    $(window).scroll(function () {

        var windowScroll = $(window).scrollTop();
        if (windowScroll > 200) {
            up.addClass("active-info");
        } else {
            up.removeClass("active-info");
        }
    });

    var box = $('#send-box');
    var btn = $('#send');
    var push = $('#push-box');
    $("#send").click(function () {
        box.addClass("active-info");
        btn.addClass('d-none');
    });

    $("#cancel-btn").click(function () {
        box.removeClass("active-info");
        btn.removeClass('d-none');
    });

    function showSendBox() {
        box.addClass("active-info");
        btn.addClass('d-none');
    }


    setTimeout(() => showSendBox(), 3000);
    var tab = document.getElementById('tab1');
    tab.setAttribute('checked', 'true');
});

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
                notice(data)
            } else {
                notice(data)
            }
        },
        error: function (data) {
            alert('error')
        }
    })
})


function notice(text) {
    // function generate(text) {
    new Noty({
        text: text,
        // type: type,
        type: 'info',
        dismissQueue: true,
        // layout: layout,
        layout: 'bottomCenter',
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

$('#btn_filter').click(function () {

    let arr_link = []

    let price_from = $('#price_from')[0].value
    let price_until = $('#price_until')[0].value
    let str_price = ''
    if (price_from || price_until) {
        str_price = 'price=' + price_from + '&' + price_until
        arr_link.push(str_price)
    }


    let resources = $("#card_resources>div").children(':checked')
    let needs = $("#card_needs>div").children(':checked')
    let brands = $("#card_brands>div").children(':checked')

    let str_resources = ''
    if (resources.length > 0) {
        let arr_resources = []
        for (let i = 0; i < resources.length; i++) {
            arr_resources.push(resources[i].dataset.res)
        }
        str_resources = 'resources=' + arr_resources.join('&')
        arr_link.push(str_resources)
    }

    let str_needs = ''
    if (needs.length > 0) {
        let arr_needs = []
        for (let i = 0; i < needs.length; i++) {
            arr_needs.push(needs[i].dataset.res)
        }
        str_needs = 'needs=' + arr_needs.join('&')
        arr_link.push(str_needs)
    }

    let str_brands = ''
    if (brands.length > 0) {
        let arr_brands = []
        for (let i = 0; i < brands.length; i++) {
            arr_brands.push(brands[i].dataset.res)
        }
        str_brands = 'brands=' + arr_brands.join('&')
        arr_link.push(str_brands)
    }
    let link = arr_link.join('%')
    console.log(link)
    if (this.dataset.filter) {
        link += '/' + this.dataset.filter + '/'
    }

    window.location.href = '/catalog/' + this.dataset.page + '/' + link
})

// $('#filter_selector').onchange(function () {
//     console.log(this.value)
// })
// let prod=document.getElementById("products").children
// price=prod[0].querySelector('small.text-muted').innerText
// name=prod[0].querySelector('h5.card-title').innerText
// id=prod[0].querySelector('a').href


$('#excel-file-admin').on('change', function () {
    var fileName = $(this).val();
    if (fileName) {
        var btn = $('#submit-excel-file-admin');
        btn.click();
    }

});

function set_footer() {
    let body = document.getElementsByTagName('body')[0].getBoundingClientRect().height
    let wind = document.documentElement.clientHeight
    if (wind > body) {
        let res2 = (wind - body) / 2;
        // $('#main_block_content').css('top', res2);
        $('#main_footer:first').addClass('absolute_footer');
    }
}

document.addEventListener("DOMContentLoaded", () => {
    set_footer()
});
window.onload = function () {

    set_footer()

}

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

function check_login() {
    let email = document.getElementById('login_email').value
    let password = document.getElementById('login_password').value
    $.ajax({
        type: "GET",
        dataType: "json",
        async: true,
        url: 'check_login',
        data: {
            email: email,
            password: password
        },
        success: function (data) {
            if (data !== true) {
                notice(data)
                return true
            } else {
                window.location.href = '/'
            }
        },
        error: function (data) {
            alert('error')
        }
    })
}

function check_register() {
    let name = document.getElementById('reg_name').value
    let surename = document.getElementById('reg_surename').value
    let patronymic = document.getElementById('reg_patronymic').value
    let phone = document.getElementById('reg_phone').value
    let email = document.getElementById('reg_email').value
    let adress = document.getElementById('reg_adress').value
    let pass1 = document.getElementById('reg_pass1').value
    let pass2 = document.getElementById('reg_pass2').value
    $.ajax({
        type: "GET",
        dataType: "json",
        async: true,
        url: 'check_register',
        data: {
            name: name,
            surename: surename,
            patronymic: patronymic,
            phone: phone,
            email: email,
            adress: adress,
            pass1: pass1,
            pass2: pass2
        },
        success: function (data) {
            if (data !== true) {
                notice(data)
            } else {
                window.location.href = '/log_in'
            }
        },
        error: function (data) {
            alert('error')
        }
    })
}

$('#search_input').keyup(function () {
    let names = this.value.split(' ').join('_')
    let form = document.getElementById('search_form').action = "/catalog/" + names + '/'
})

$('#btn_add_to_cart').click(function () {
    let slug = this.dataset.slug
    let count = document.getElementById('item_count').value
    $.ajax({
        type: "GET",
        dataType: "json",
        async: true,
        url: '/cart/add_product',
        data: {
            slug: slug,
            count: count
        },
        success: function (data) {
            if (data !== false) {
                // notice(data)
                document.getElementById('user_basket_total').innerText = 'Корзина ' + data + ' руб.'
            } else {
                notice(data)
            }
        },
        error: function (data) {
            alert('error')
        }
    })
})
$('.btn_cart_minus').on('click', function () {
    let elem=this
    let slug = elem.dataset.slug
    let minus = 1
    $.ajax({
        type: "GET",
        dataType: "json",
        async: true,
        url: '/cart/add_product',
        data: {
            slug: slug,
            minus: minus
        },
        success: function (data) {
            if (data[0] !== false) {
                elem.nextSibling.value=data[1]
                document.getElementById('item_'+slug).innerText=data[0]+ ' руб.'
                document.getElementById('user_basket_total').innerText = 'Корзина ' + data[2] + ' руб.'
                document.getElementById('cart_total_price').innerText = data[2] + ' руб.'
            } else {
                notice(data)
            }
        },
        error: function (data) {
            alert('error')
        }
    })
})
$('.btn_cart_plus').on('click', function () {
    let elem=this
    let slug = elem.dataset.slug
    $.ajax({
        type: "GET",
        dataType: "json",
        async: true,
        url: '/cart/add_product',
        data: {
            slug: slug
            // minus: minus
        },
        success: function (data) {
            if (data[0] !== false) {
                elem.previousSibling.value=data[1]
                document.getElementById('item_'+slug).innerText=data[0]+ ' руб.'
                document.getElementById('user_basket_total').innerText = 'Корзина ' + data[2] + ' руб.'
                document.getElementById('cart_total_price').innerText = data[2] + ' руб.'
            } else {
                notice(data)
            }
        },
        error: function (data) {
            alert('error')
        }
    })
})

$('.btn_cart_del_item').on('click', function () {
    let elem=this
    let slug = elem.dataset.slug
    $.ajax({
        type: "GET",
        dataType: "json",
        async: true,
        url: '/cart/add_product',
        data: {
            slug: slug,
            del:1
            // minus: minus
        },
        success: function (data) {
            if (data !== false) {
                document.getElementById('carditem_'+slug).remove()
                // elem.previousSibling.value=data[1]
                // document.getElementById('item_'+slug).innerText=data[0]+ ' руб.'
                document.getElementById('user_basket_total').innerText = 'Корзина ' + data + ' руб.'
                document.getElementById('cart_total_price').innerText = data + ' руб.'
            } else {
                notice(data)
            }
        },
        error: function (data) {
            alert('error')
        }
    })
})