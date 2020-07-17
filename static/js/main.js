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


    setTimeout(() => showSendBox(), 5000);
});

$('.multiple-items').slick({
    accessibility: true,
    autoplay: true,
    arrows: true,
    dots: false,
    infinite: true,
    nextArrow: '<i class="fa fa-angle-right next" aria-hidden="true"></i>',
    prevArrow: '<i class="fa fa-angle-left prev" aria-hidden="true"></i>',
    speed: 1000,
    //количество отображаемых слайдов
    slidesToShow: 4,
    //сколько слайдов отображать за раз при прокручивании
    slidesToScroll: 1,
    lazyLoad: 'ondemand',
    pauseOnHover: true,
    responsive: [
        {
            breakpoint: 1024,
            settings: {
                pauseOnHover: true,
                autoplay: true,
                slidesToShow: 3,
                slidesToScroll: 1,
                infinite: true,
                dots: false,
                lazyLoad: 'ondemand'
            }
        },
        {
            breakpoint: 600,
            settings: {
                pauseOnHover: true,
                autoplay: true,
                infinite: true,
                slidesToShow: 2,
                slidesToScroll: 1,
                dots: false,
                lazyLoad: 'progressive'
            }
        },
        {
            breakpoint: 480,
            settings: {
                pauseOnHover: true,
                autoplay: true,
                infinite: true,
                slidesToShow: 2,
                slidesToScroll: 1,
                dots: false,
                lazyLoad: 'progressive'
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
    new Noty({
        text: text,
        // type: type,
        type: 'info',
        dismissQueue: true,
        // layout: layout,
        layout: 'bottomCenter',
        theme: 'relax'
    }).show();
}

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
        // var $input = $(this).parent().find('input');
        // if ($input[0].max <= parseInt($input.val()) + 1) {
        //     $input.val(parseInt($input.val()) + 1);
        //     $input.change();
        // }
        let input = this.previousElementSibling
        let max = input.max
        let val = parseInt(input.value)
        if (max >= val + 1) {
            input.value = val + 1
        }
        return false;
    });
});

function check_input_count_prod(elem) {

    try {
        if (parseInt(elem.value) > parseInt(elem.max)) {
            // if (inp > parseInt(elem.max)|| !inp&&parseFloat(elem.value) != parseInt(elem.value) || !inp ) {
            elem.value = elem.max
        }
    } catch (e) {
        elem.value = elem.max
    }
}


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
$('#image-file-admin').on('change', function () {
    var fileName = $(this).val();
    if (fileName) {
        var btn = $('#submit-image-file-admin');
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

$('#select_product_sizes').change(function () {
    // alert(this.selectedOptions[0].value)
    let id = this.value
    if (document.getElementById('item_count')) {
        document.getElementById('item_count').max = this.selectedOptions[0].dataset.count
    }

    if (parseInt(this.selectedOptions[0].dataset.sale) > 0) {
        // try {
        //     document.getElementById('is_sale_prod').removeAttribute('class', 'd-none')
        // } catch (e) {
        //
        // }
        $("#is_sale_prod").toggleClass('d-none', false).toggleClass('d-inline-block', true);
        // $( "#is_sale_prod" ).toggleClass( 'd-inline-block' );

        // document.getElementById('is_sale_prod').setAttribute('class', 'd-inline-block')
        let i = document.createElement('i')
        i.setAttribute('class', 'fa fa-tag')
        i.setAttribute('aria-hidden', 'true')
        let small = document.createElement('small')
        small.setAttribute('class', 'old-price-card')
        small.setAttribute('id', 'product_sale')
        document.getElementById('is_sale_prod').appendChild(i)
        document.getElementById('is_sale_prod').appendChild(small)
        document.getElementById('product_sale').innerText = this.selectedOptions[0].dataset.sale + ' руб.'
    } else {
        // try {
        //     document.getElementById('is_sale_prod').removeAttribute('class', 'd-inline-block')
        // } catch (e) {
        //
        // }
        //
        // document.getElementById('is_sale_prod').setAttribute('class', 'd-none mr-5')
        $("#is_sale_prod").toggleClass('d-none', true).toggleClass('d-inline-block', false);
        document.getElementById('is_sale_prod').innerHTML = ''
        // document.getElementById('product_sale').innerText = 0
    }
    if (parseInt(this.selectedOptions[0].dataset.count) > 0) {
        document.getElementById('item_count').value = 1
        document.getElementById('product_price').innerText = this.selectedOptions[0].dataset.price + ' руб.'
        document.getElementById('prod_input').style.display = 'block'
        document.getElementById('prod_button').style.display = 'block'
    } else {
        // document.getElementById('item_count').value = 0
        document.getElementById('product_price').innerText = 'К сожалению, товара нет в наличии.'
        document.getElementById('prod_input').style.display = 'none'
        document.getElementById('prod_button').style.display = 'none'
    }

    // let price=0
    // for (let i=0;i<prod_sizes.length;i++){
    //     if(prod_sizes[i].size_id==id){
    //         document.getElementById('product_price').innerText=prod_sizes[i].price
    //     }
    // }
})


document.addEventListener("DOMContentLoaded", () => {
    set_footer()
    // if (document.getElementById('btn_add_to_cart')) {
    //     get_prod_sizes()
    // }
});
window.onload = function () {
    set_footer()

    // if (document.getElementById('btn_add_to_cart')) {
    //     get_prod_sizes()
    // }

}

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

$('.custom-control-input').change(function () {
    if ($(this).is(':checked')) {
        $('.change-pass_blk').fadeIn(100);
    } else {
        $('.change-pass_blk').fadeOut(200);
    }
});

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
    let count = document.getElementById('item_count').value
    let prod_size = document.getElementById('select_product_sizes')
    if (prod_size) {
        prod_size = prod_size.value
    } else {
        prod_size = this.dataset.slug
    }
    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        url: '/cart/add_product',
        data: {
            count: count,
            prod_size: prod_size
        },
        success: function (data) {
            if (data !== false) {
                document.getElementById('user_basket_total').innerText = data + ' руб.'
                notice('Добавлено в корзину')
            } else {
                notice('Не удалось добавить в корзину, попробуйте позже!')
            }
        },
        error: function (data) {
            alert('error')
        }
    })
})
$('.btn_cart_minus').on('click', function () {
    let elem = this
    let slug = elem.parentElement.dataset.slug
    if (parseInt(this.nextElementSibling.value) >= 1) {
        $.ajax({
            type: "GET",
            dataType: "json",
            async: false,
            url: '/cart/plus_minus_product',
            data: {
                slug: slug,
                minus: 1
            },
            success: function (data) {
                if (data !== false) {
                    elem.nextSibling.value = data.prod_count
                    document.getElementById('item_' + slug).innerText = data.product_total + ' руб.'
                    document.getElementById('user_basket_total').innerText = data.total + ' руб.'
                    document.getElementById('cart_total_price').innerText = data.total + ' руб.'
                } else {
                    notice('Произошла ошибка, попробуйте позже!')
                }
            },
            error: function (data) {
                alert('error')
            }
        })
    }
})
$('.btn_cart_plus').on('click', function () {
    let elem = this
    let slug = elem.parentElement.dataset.slug
    if (parseInt(this.previousElementSibling.value) <= parseInt(this.previousElementSibling.max)) {
        $.ajax({
            type: "GET",
            dataType: "json",
            async: false,
            url: '/cart/plus_minus_product',
            data: {
                slug: slug
            },
            success: function (data) {
                if (data !== false) {
                    elem.previousSibling.value = data.prod_count
                    document.getElementById('item_' + slug).innerText = data.product_total + ' руб.'
                    document.getElementById('user_basket_total').innerText = data.total + ' руб.'
                    document.getElementById('cart_total_price').innerText = data.total + ' руб.'
                } else {
                    notice('Произошла ошибка, попробуйте позже!')
                }
            },
            error: function (data) {
                alert('error')
            }
        })
    }
})

$('.btn_cart_del_item').on('click', function () {
    let slug = this.dataset.slug
    $.ajax({
        type: "GET",
        dataType: "json",
        async: true,
        url: '/cart/del_product',
        data: {
            slug: slug
        },
        success: function (data) {
            if (data !== false) {
                document.getElementById('carditem_' + slug).remove()
                document.getElementById('user_basket_total').innerText = data + ' руб.'
                document.getElementById('cart_total_price').innerText = data + ' руб.'
            } else {
                notice('Произошла ошибка, попробуйте позже!')
            }
        },
        error: function (data) {
            alert('error')
        }
    })
})

// function check_input_count_prod(elem) {
//
//     try {
//         if (parseInt(elem.value) > parseInt(elem.max)) {
//             // if (inp > parseInt(elem.max)|| !inp&&parseFloat(elem.value) != parseInt(elem.value) || !inp ) {
//             elem.value = elem.max
//         }
//     } catch (e) {
//         elem.value = elem.max
//     }
// }

$('.cart_item_input').on('keyup', function () {
    let elem = this
    let slug = elem.parentElement.dataset.slug
    let count = this.value
    if (parseInt(this.value) <= parseInt(this.max)) {
        $.ajax({
            type: "GET",
            dataType: "json",
            async: true,
            url: '/cart/plus_minus_product',
            data: {
                slug: slug,
                count: count
            },
            success: function (data) {
                if (data !== false) {
                    elem.innerText = data.prod_count
                    document.getElementById('item_' + slug).innerText = data.product_total + ' руб.'
                    document.getElementById('user_basket_total').innerText = data.total + ' руб.'
                    document.getElementById('cart_total_price').innerText = data.total + ' руб.'
                } else {
                    notice('Произошла ошибка, попробуйте позже!')
                }
            },
            error: function (data) {
                alert('error')
            }
        })
    } else {
        this.value = this.max
    }
})

$('#btn_change_contact_details').click(function () {
    let name = document.getElementById('cd_name').value
    let surname = document.getElementById('cd_surname').value
    let patron = document.getElementById('cd_patron').value
    // let email =  document.getElementById('cd_email').value
    let phone = document.getElementById('cd_phone').value
    // let address =  document.getElementById('cd_address').value
    let pass1 = document.getElementById('cd_pass1').value
    let pass2 = document.getElementById('cd_pass2').value
    let pass3 = document.getElementById('cd_pass3').value
    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        url: '/profile/change_contact_details',
        data: {
            name: name,
            surname: surname,
            patron: patron,
            // email: email,
            phone: phone,
            // address: address,
            pass1: pass1,
            pass2: pass2,
            pass3: pass3
        },
        success: function (data) {
            if (data !== false) {
                notice(data)
                // document.getElementById('user_basket_total').innerText = data + ' руб.'
                // notice('Добавлено в корзину')
            } else {
                // notice('Произошла ошибка, попробуйте позже!')
                window.location.href = '/log_in'
            }
        },
        error: function (data) {
            alert('error')
        }
    })
})

$('#btn_change_address').click(function () {
    let city = document.getElementById('da_city').value
    let street = document.getElementById('da_street').value
    let house = document.getElementById('da_house').value
    let flat = document.getElementById('da_flat').value
    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        url: '/profile/change_address',
        data: {
            city: city,
            street: street,
            house: house,
            flat: flat
        },
        success: function (data) {
            if (data !== false) {
                notice(data)
                // document.getElementById('user_basket_total').innerText = data + ' руб.'
                // notice('Добавлено в корзину')
            } else {
                // notice('Произошла ошибка, попробуйте позже!')
                window.location.href = '/log_in'
            }
        },
        error: function (data) {
            alert('error')
        }
    })
})

$('#btn_buy_products').click(function () {
    // let city = document.getElementById('da_city').value
    // let street = document.getElementById('da_street').value
    // let house = document.getElementById('da_house').value
    // let flat = document.getElementById('da_flat').value
    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        url: '/cart/buy_products',
        data: {
            // city: city,
            // street: street,
            // house: house,
            // flat: flat
        },
        success: function (data) {
            if (data !== false) {
                notice(data)
                // document.getElementById('user_basket_total').innerText = data + ' руб.'
                // notice('Добавлено в корзину')
            } else {
                // notice('Произошла ошибка, попробуйте позже!')
                window.location.href = '/log_in'
            }
        },
        error: function (data) {
            alert('error')
        }
    })
});
$('#FIO').click(function () {
    document.getElementById('FIO').classList.remove('is-invalid');
    document.getElementById('FIO').classList.remove('is-valid');
});
$('#address').click(function () {
    document.getElementById('address').classList.remove('is-invalid');
    document.getElementById('address').classList.remove('is-valid');
});
$('#email').click(function () {
    document.getElementById('email').classList.remove('is-invalid');
    document.getElementById('email').classList.remove('is-valid');
});
$('#tel').click(function () {
    document.getElementById('tel').classList.remove('is-invalid');
    document.getElementById('tel').classList.remove('is-valid');
});
$('#conf-btn').click(function () {
    var fio = document.getElementById('FIO').value;
    var address = document.getElementById('address').value;
    var email = document.getElementById('email').value;
    var tel = document.getElementById('tel').value;
    if (fio !== "" && address !== "" && email !== "" && tel !== "") {
        document.getElementById('FIO').classList.add('is-valid');
        document.getElementById('address').classList.add('is-valid');
        document.getElementById('email').classList.add('is-valid');
        document.getElementById('tel').classList.add('is-valid');
        document.getElementById('conf-btn-sub').click();

        // $.ajax({
        //     type: "GET",
        //     url: '/cart/confirm_order',
        //     data: {
        //         fio: fio,
        //         address: address,
        //         email: email,
        //         tel: tel
        //     },
        //     success: function (data) {
        //         // if (data !== false) {
        //         //     notice(data)
        //         //     // document.getElementById('user_basket_total').innerText = data + ' руб.'
        //         //     // notice('Добавлено в корзину')
        //         // } else {
        //         //     // notice('Произошла ошибка, попробуйте позже!')
        //         //     window.location.href = '/log_in'
        //         // }
        //     },
        //     error: function (data) {
        //         alert('error')
        //     }
        // })
    } else {
        if (fio !== "")
            document.getElementById('FIO').classList.add('is-valid');
        else
            document.getElementById('FIO').classList.add('is-invalid');
        if (address !== "")
            document.getElementById('address').classList.add('is-valid');
        else
            document.getElementById('address').classList.add('is-invalid');
        if (email !== "")
            document.getElementById('email').classList.add('is-valid');
        else
            document.getElementById('email').classList.add('is-invalid');
        if (tel !== "")
            document.getElementById('tel').classList.add('is-valid');
        else
            document.getElementById('tel').classList.add('is-invalid');
        notice("Заполнены не все поля");
    }
});

$('#btn_final_pay').click(function () {
    // let el = document.getElementById('pay_values')

    // let slug = elem.parentElement.dataset.slug
    // if (parseInt(this.previousElementSibling.value) <= parseInt(this.previousElementSibling.max)) {
        $.ajax({
            type: "GET",
            dataType: "json",
            async: false,
            url: '/cart/pay_check',
            success: function (data) {
                console.log(data)
                let el=document.getElementById('pay_values')
                el.setAttribute('onclick','Robokassa.StartPayment({' +
                    'MerchantLogin: \''+data.MerchantLogin+'\',' +
                    'OutSum: \''+data.OutSum+'\',' +
                    'Description: \'Оплата на сайте The Care\',' +
                    // 'Shp_User: \''+data.Shp_user+'\',' +
                    'Culture: \'ru\',' +
                    'Encoding: \'utf-8\',' +
                    'IsTest: \'1\',' +
                    'SignatureValue: \''+data.SignatureValue+'\'})' )
                el.click()
            },
            error: function (data) {
                alert('error')
            }
        })
    // }
})