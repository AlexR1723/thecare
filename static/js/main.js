function notice(e) {
    new Noty({text: e, type: "info", dismissQueue: !0, layout: "bottomCenter", theme: "relax"}).show()
}

function check_input_count_prod(e) {
    try {
        parseInt(e.value) > parseInt(e.max) && (e.value = e.max)
    } catch (t) {
        e.value = e.max
    }
}

function set_footer() {
    let e = document.getElementsByTagName("body")[0].getBoundingClientRect().height,
        t = document.documentElement.clientHeight;
    if (t > e) {
        $("#main_footer:first").addClass("absolute_footer")
    }
}

function check_login() {
    let e = document.getElementById("login_email").value, t = document.getElementById("login_password").value;
    $.ajax({
        type: "GET",
        dataType: "json",
        async: !0,
        url: "check_login",
        data: {email: e, password: t},
        success: function (e) {
            if (!0 !== e) return notice(e), !0;
            window.location.href = "/"
        },
        error: function (e) {
            alert("error")
        }
    })
}

function check_register() {
    let e = document.getElementById("reg_name").value, t = document.getElementById("reg_surename").value,
        n = document.getElementById("reg_patronymic").value, a = document.getElementById("reg_phone").value,
        s = document.getElementById("reg_email").value, l = document.getElementById("reg_adress").value,
        o = document.getElementById("reg_pass1").value, i = document.getElementById("reg_pass2").value;
    $.ajax({
        type: "GET",
        dataType: "json",
        async: !0,
        url: "check_register",
        data: {name: e, surename: t, patronymic: n, phone: a, email: s, adress: l, pass1: o, pass2: i},
        success: function (e) {
            !0 !== e ? notice(e) : window.location.href = "/log_in"
        },
        error: function (e) {
            alert("error")
        }
    })
}

jQuery("document").ready(function (e) {
    var t = e("#block-up");
    e(window).scroll(function () {
        e(window).scrollTop() > 200 ? t.addClass("active-info") : t.removeClass("active-info")
    });
    var n = e("#send-box"), a = e("#send");
    e("#push-box");

    function s() {
        n.addClass("active-info"), a.addClass("d-none")
    }

    e("#send").click(function () {
        n.addClass("active-info"), a.addClass("d-none")
    }), e("#cancel-btn").click(function () {
        n.removeClass("active-info"), a.removeClass("d-none")
    }), setTimeout(() => s(), 5e3), setInterval(() => {
        n.removeClass("active-info"), a.removeClass("d-none"), setTimeout(() => s(), 12e4)
    }, 12e4)
}), $(".multiple-items").slick({
    accessibility: !0,
    arrows: !0,
    dots: !1,
    infinite: !0,
    nextArrow: '<i class="fa fa-angle-right next" aria-hidden="true"></i>',
    prevArrow: '<i class="fa fa-angle-left prev" aria-hidden="true"></i>',
    speed: 1e3,
    slidesToShow: 4,
    slidesToScroll: 1,
    lazyLoad: "ondemand",
    pauseOnHover: !0,
    responsive: [{
        breakpoint: 1024,
        settings: {pauseOnHover: !0, slidesToShow: 3, slidesToScroll: 1, infinite: !0, dots: !1, lazyLoad: "ondemand"}
    }, {
        breakpoint: 600,
        settings: {pauseOnHover: !0, infinite: !0, slidesToShow: 2, slidesToScroll: 1, dots: !1, lazyLoad: "ondemand"}
    }, {
        breakpoint: 480,
        settings: {pauseOnHover: !0, infinite: !0, slidesToShow: 2, slidesToScroll: 1, dots: !1, lazyLoad: "ondemand"}
    }]
}), $("#send_feedback").click(function () {
    let e = $("#feedback_name")[0].value, t = $("#feedback_email")[0].value, n = $("#feedback_subject")[0].value,
        a = $("#feedback_text")[0].value;
    $.ajax({
        type: "GET",
        dataType: "json",
        async: !0,
        url: "send_feedback",
        data: {name: e, email: t, subject: n, text: a},
        success: function (e) {
            notice(e)
        },
        error: function (e) {
            alert("error")
        }
    })
}), $(".items-counter").ready(function () {
    $(".minus").click(function () {
        var e = $(this).parent().find("input"), t = parseInt(e.val()) - 1;
        return t = t < 1 ? 1 : t, e.val(t), e.change(), !1
    }), $(".plus").click(function () {
        let e = this.previousElementSibling, t = e.max, n = parseInt(e.value);
        return t >= n + 1 && (e.value = n + 1), !1
    })
}), $("#btn_filter").click(function () {
    let e = [], t = $("#price_from")[0].value, n = $("#price_until")[0].value, a = "";
    (t || n) && (a = "price=" + t + "&" + n, e.push(a));
    let s = $("#card_resources>div").children(":checked"), l = $("#card_needs>div").children(":checked"),
        o = $("#card_brands>div").children(":checked"), i = "";
    if (s.length > 0) {
        let t = [];
        for (let e = 0; e < s.length; e++) t.push(s[e].dataset.res);
        i = "resources=" + t.join("&"), e.push(i)
    }
    let c = "";
    if (l.length > 0) {
        let t = [];
        for (let e = 0; e < l.length; e++) t.push(l[e].dataset.res);
        c = "needs=" + t.join("&"), e.push(c)
    }
    let d = "";
    if (o.length > 0) {
        let t = [];
        for (let e = 0; e < o.length; e++) t.push(o[e].dataset.res);
        d = "brands=" + t.join("&"), e.push(d)
    }
    let u = e.join("%");
    console.log(u), this.dataset.filter && (u += "/" + this.dataset.filter + "/"), window.location.href = "/catalog/" + this.dataset.page + "/" + u
}), $("#excel-file-admin").on("change", function () {
    $(this).val() && $("#submit-excel-file-admin").click()
}), $("#image-file-admin").on("change", function () {
    $(this).val() && $("#submit-image-file-admin").click()
}),
    $('#select_product_sizes').change(function () {
        // alert(this.selectedOptions[0].value)
        if (document.getElementById('select_product_sizes').dataset.tone == "True") {
            let prod_id = this.selectedOptions[0].value
            $.ajax({
                type: "GET",
                dataType: "json",
                async: true,
                url: 'get_sizes_by_id',
                data: {
                    prod_id: prod_id
                },
                success: function (data) {
                    if (data !== false) {
                        let select = document.getElementById('select_product_tone')
                        select.innerHTML = '';
                        for (let i = 0; i < data.length; i++) {
                            let el = data[i]
                            let opt = document.createElement('option');
                            opt.setAttribute('value', el.id);
                            opt.setAttribute('data-price', el.price);
                            opt.setAttribute('data-sale', el.sale);
                            opt.setAttribute('data-count', el.count);
                            opt.setAttribute('data-old_price', el.old_price);
                            if (parseInt(el.sale) > 0) {
                                opt.innerText = el.tone + ' -' + el.sale + '%'
                            } else {
                                opt.innerText = el.tone
                            }
                            select.appendChild(opt)
                        }
                        // select.change()
                        $("#select_product_tone").trigger('change');
                    } else {
                        notice('Произошла ошибка, попробуйте позже.')
                    }
                },
                error: function (data) {
                    alert('error')
                }
            })
        } else {
            // let id = this.value
            if (document.getElementById('item_count')) {
                document.getElementById('item_count').max = this.selectedOptions[0].dataset.count
            }
            if (parseInt(this.selectedOptions[0].dataset.sale) > 0) {
                $("#is_sale_prod").toggleClass('d-none', false).toggleClass('d-inline-block', true);
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
                $("#is_sale_prod").toggleClass('d-none', true).toggleClass('d-inline-block', false);
                document.getElementById('is_sale_prod').innerHTML = ''
            }
            if (parseInt(this.selectedOptions[0].dataset.count) > 0) {
                document.getElementById('item_count').value = 1
                document.getElementById('product_price').innerText = this.selectedOptions[0].dataset.price + ' руб.'
                document.getElementById('prod_input').style.display = 'block'
                document.getElementById('prod_button').style.display = 'block'
            } else {
                document.getElementById('product_price').innerText = 'К сожалению, товара нет в наличии.'
                document.getElementById('prod_input').style.display = 'none'
                document.getElementById('prod_button').style.display = 'none'
            }
        }
    })


$('#select_product_tone').change(function () {
    let prod_id = this.selectedOptions[0].value

    if (document.getElementById('item_count')) {
        document.getElementById('item_count').max = this.selectedOptions[0].dataset.count
    }
    if (parseInt(this.selectedOptions[0].dataset.sale) > 0) {
        $("#is_sale_prod").toggleClass('d-none', false).toggleClass('d-inline-block', true);
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
        $("#is_sale_prod").toggleClass('d-none', true).toggleClass('d-inline-block', false);
        document.getElementById('is_sale_prod').innerHTML = ''
    }
    if (parseInt(this.selectedOptions[0].dataset.count) > 0) {
        document.getElementById('item_count').value = 1
        document.getElementById('product_price').innerText = this.selectedOptions[0].dataset.price + ' руб.'
        document.getElementById('prod_input').style.display = 'block'
        document.getElementById('prod_button').style.display = 'block'
    } else {
        document.getElementById('product_price').innerText = 'К сожалению, товара нет в наличии.'
        document.getElementById('prod_input').style.display = 'none'
        document.getElementById('prod_button').style.display = 'none'
    }

})


document.addEventListener("DOMContentLoaded", () => {
    set_footer()
}), window.onload = function () {
    set_footer()
}, $(function () {
    $('[data-toggle="tooltip"]').tooltip()
}), $(".custom-control-input").change(function () {
    $(this).is(":checked") ? $(".change-pass_blk").fadeIn(100) : $(".change-pass_blk").fadeOut(200)
}), $("#search_input").keyup(function () {
    let e = this.value.split(" ").join("_");
    document.getElementById("search_form").action = "/catalog/" + e + "/"
}),
    $("#btn_add_to_cart").click(function () {
        let count = document.getElementById('item_count').value
        let prod_size = document.getElementById('select_product_sizes')
        if (prod_size.dataset.tone === "True") {
            prod_size=document.getElementById('select_product_tone').value
        } else {

            if (prod_size) {
                prod_size = prod_size.value
            } else {
                prod_size = this.dataset.slug
            }
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
                    document.getElementById('user_basket_total').innerText = data[0] + ' руб.'
                    document.getElementById('count_user_items').innerHTML = data[1]
                    notice('Добавлено в корзину')
                } else {
                    notice('Не удалось добавить в корзину, попробуйте позже!')
                }
            },
            error: function (data) {
                alert('error')
            }
        })

    }),
    $(".btn_cart_minus").on("click", function () {
        let e = this, t = e.parentElement.dataset.slug;
        parseInt(this.nextElementSibling.value) >= 2 && $.ajax({
            type: "GET",
            dataType: "json",
            async: !1,
            url: "/cart/plus_minus_product",
            data: {slug: t, minus: 1},
            success: function (n) {
                !1 !== n ? (e.nextSibling.value = n.prod_count, document.getElementById("item_" + t).innerText = n.product_total + " руб.", document.getElementById("user_basket_total").innerText = n.total + " руб.", document.getElementById("cart_total_price").innerText = n.total + " руб.", document.getElementById("count_user_items").innerHTML = n.cnt) : notice("Произошла ошибка, попробуйте позже!")
            },
            error: function (e) {
                alert("error")
            }
        })
    }), $(".btn_cart_plus").on("click", function () {
    let e = this, t = e.parentElement.dataset.slug;
    parseInt(this.previousElementSibling.value) < parseInt(this.previousElementSibling.max) && $.ajax({
        type: "GET",
        dataType: "json",
        async: !1,
        url: "/cart/plus_minus_product",
        data: {slug: t},
        success: function (n) {
            !1 !== n ? (e.previousSibling.value = n.prod_count, document.getElementById("item_" + t).innerText = n.product_total + " руб.", document.getElementById("user_basket_total").innerText = n.total + " руб.", document.getElementById("cart_total_price").innerText = n.total + " руб.", document.getElementById("count_user_items").innerHTML = n.cnt) : notice("Произошла ошибка, попробуйте позже!")
        },
        error: function (e) {
            alert("error")
        }
    })
}), $(".btn_cart_del_item").on("click", function () {
    let e = this.dataset.slug;
    $.ajax({
        type: "GET", dataType: "json", async: !0, url: "/cart/del_product", data: {slug: e}, success: function (t) {
            !1 !== t ? (document.getElementById("carditem_" + e).remove(), document.getElementById("user_basket_total").innerText = t[0] + " руб.", document.getElementById("cart_total_price").innerText = t[0] + " руб.", document.getElementById("count_user_items").innerHTML = t[1]) : notice("Произошла ошибка, попробуйте позже!")
        }, error: function (e) {
            alert("error")
        }
    })
}), $(".cart_item_input").on("keyup", function () {
    let e = this, t = e.parentElement.dataset.slug, n = this.value;
    this.value || (n = 0), parseInt(this.value) > parseInt(this.max) && (this.value = this.max, n = this.max), $.ajax({
        type: "GET",
        dataType: "json",
        async: !0,
        url: "/cart/plus_minus_product",
        data: {slug: t, count: n},
        success: function (n) {
            !1 !== n ? (e.innerText = n.prod_count, document.getElementById("item_" + t).innerText = n.product_total + " руб.", document.getElementById("user_basket_total").innerText = n.total + " руб.", document.getElementById("cart_total_price").innerText = n.total + " руб.", document.getElementById("count_user_items").innerHTML = n.cnt) : notice("Произошла ошибка, попробуйте позже!")
        },
        error: function (e) {
            alert("error")
        }
    })
}), $("#btn_change_contact_details").click(function () {
    let e = document.getElementById("cd_name").value, t = document.getElementById("cd_surname").value,
        n = document.getElementById("cd_patron").value, a = document.getElementById("cd_phone").value,
        s = document.getElementById("cd_pass1").value, l = document.getElementById("cd_pass2").value,
        o = document.getElementById("cd_pass3").value;
    $.ajax({
        type: "GET",
        dataType: "json",
        async: !1,
        url: "/profile/change_contact_details",
        data: {name: e, surname: t, patron: n, phone: a, pass1: s, pass2: l, pass3: o},
        success: function (e) {
            !1 !== e ? notice(e) : window.location.href = "/log_in"
        },
        error: function (e) {
            alert("error")
        }
    })
}), $("#btn_change_address").click(function () {
    let e = document.getElementById("da_city").value, t = document.getElementById("da_street").value,
        n = document.getElementById("da_house").value, a = document.getElementById("da_flat").value;
    $.ajax({
        type: "GET",
        dataType: "json",
        async: !1,
        url: "/profile/change_address",
        data: {city: e, street: t, house: n, flat: a},
        success: function (e) {
            !1 !== e ? notice(e) : window.location.href = "/log_in"
        },
        error: function (e) {
            alert("error")
        }
    })
}), $("#FIO").click(function () {
    document.getElementById("FIO").classList.remove("is-invalid"), document.getElementById("FIO").classList.remove("is-valid")
}), $("#address").click(function () {
    document.getElementById("address").classList.remove("is-invalid"), document.getElementById("address").classList.remove("is-valid")
}), $("#email").click(function () {
    document.getElementById("email").classList.remove("is-invalid"), document.getElementById("email").classList.remove("is-valid")
}), $("#tel").click(function () {
    document.getElementById("tel").classList.remove("is-invalid"), document.getElementById("tel").classList.remove("is-valid")
}), $("#conf-btn").click(function () {
    var e = document.getElementById("FIO").value, t = document.getElementById("address").value,
        n = document.getElementById("email").value, a = document.getElementById("tel").value;
    "" !== e && "" !== t && "" !== n && "" !== a ? (document.getElementById("FIO").classList.add("is-valid"), document.getElementById("address").classList.add("is-valid"), document.getElementById("email").classList.add("is-valid"), document.getElementById("tel").classList.add("is-valid"), document.getElementById("conf-btn-sub").click()) : ("" !== e ? document.getElementById("FIO").classList.add("is-valid") : document.getElementById("FIO").classList.add("is-invalid"), "" !== t ? document.getElementById("address").classList.add("is-valid") : document.getElementById("address").classList.add("is-invalid"), "" !== n ? document.getElementById("email").classList.add("is-valid") : document.getElementById("email").classList.add("is-invalid"), "" !== a ? document.getElementById("tel").classList.add("is-valid") : document.getElementById("tel").classList.add("is-invalid"), notice("Заполнены не все поля"))
}), $("#btn_final_pay").click(function () {
    $.ajax({
        type: "GET", dataType: "json", async: !1, url: "/cart/pay_check", success: function (e) {
            console.log(e);
            let t = document.getElementById("pay_values");
            t.setAttribute("onclick", "Robokassa.StartPayment({MerchantLogin: '" + e.MerchantLogin + "',OutSum: '" + e.OutSum + "',Description: 'Оплата на сайте The Care',InvoiceID: '" + e.InvoiceID + "',Shp_User: '" + e.Shp_user + "',Culture: 'ru',Encoding: 'utf-8',SignatureValue: '" + e.SignatureValue + "'})"), t.click()
        }, error: function (e) {
            alert("error")
        }
    })
});