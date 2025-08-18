/*var wid = $(window).width(),
hei = $(window).height();
alert("width:" + wid +"px and height: " + hei + "px.")
*/

$(document).ready(function () {
    /*function bannerheight(){
        var head_height = $("header").outerHeight(true);
        $("body").css("padding-top",head_height + "px")
        $(".banner-sec").css("min-height","calc(100vh - " + head_height + "px)")
    };
    bannerheight();
    $(window).resize(bannerheight);*/

    $(".navbar-toggler").click(function () {
        $('html').toggleClass('show-menu');
    });

    function scrolling() {
        var sticky = $('header'),
            scroll = $(window).scrollTop();

        if (scroll >= 15) sticky.addClass('fixed');
        else sticky.removeClass('fixed');
    };
    scrolling();
    $(window).scroll(scrolling);

    // hide #back-top first
    $("#myBtn").hide();

    // fade in #back-top
    $(function () {
        $(window).scroll(function () {
            if ($(this).scrollTop() > 100) {
                $('#myBtn').fadeIn();
            } else {
                $('#myBtn').fadeOut();
            }
        });

        // scroll body to 0px on click
        $('#myBtn').click(function () {
            $('body,html').animate({
                scrollTop: 0
            }, 1000);
            return false;
        });
    });

});


//cursor



$('.menu').click(function () {
    $(this).toggleClass('open');
});





$('#HeroSlider').owlCarousel({
    smartSpeed: 1450,
    items: 1,
    loop: true,
    autoplay: true,
    smartSpeed: 600,
    // autoplayTimeout: 5000,
    autoplayHoverPause: true,
    stagePadding: 0,
    nav: false,
    responsive: {
        0: {
            items: 1,
            nav: false
        },
        600: {
            items: 1,
            nav: false
        },
        1000: {
            items: 1,
            // loop: false
        }
    }
});



$('#HeroSliderRTL').owlCarousel({
    smartSpeed: 1450,
    items: 1,
    loop: true,
    autoplay: true,
    rtl: true,
    smartSpeed: 600,
    autoplay: true,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    stagePadding: 0,
    nav: false,
    responsive: {
        0: {
            items: 1,
            nav: false
        },
        600: {
            items: 1,
            nav: false
        },
        1000: {
            items: 1,
            // loop: false
        }
    }
});



$('#brand').owlCarousel({

    smartSpeed: 1450,
    items: 7,
    loop: true,
    autoplay: true,
    smartSpeed: 600,
    autoplay: true,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    margin: 30,
    stagePadding: 30,
    nav: false,
    responsive: {
        0: {
            items: 2.5,
            nav: false
        },
        600: {
            items: 5,
            nav: false
        },
        1000: {
            items: 7,
            nav: true,
            // loop: false
        }
    }
});


var serviceCarousel = $('#Services');
var serviceItemcount = serviceCarousel.find('.owl-item').length;

serviceCarousel.owlCarousel({
    loop: serviceItemcount > 3,
    margin: 54,
    autoplay: true,
    smartSpeed: 600,
    autoplay: true,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    nav: true,
    navText: ["<img src='https://rakhospital.com/wp-content/themes/rak-hospital/assets/images/left-chevron.png'>", "<img src='https://rakhospital.com/wp-content/themes/rak-hospital/assets/images/chevron.png'>"],
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: true
        },
        600: {
            items: 2,
            nav: true
        },
        1000: {
            items: 3,
            nav: true,
            // loop: false
        }
    }
})

$('#testiSlider').owlCarousel({
    loop: true,
    margin: 54,
    autoplay: true,
    smartSpeed: 600,
    // autoplay: true,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    nav: true,
    navText: ["<img src='https://rakhospital.com/wp-content/themes/rak-hospital/assets/images/left-chevron.png'>", "<img src='https://rakhospital.com/wp-content/themes/rak-hospital/assets/images/chevron.png'>"],
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: true
        },
        600: {
            items: 2,
            nav: true
        },

        800: {
            items: 2,
            nav: true
        },

        1000: {
            items: 3,
            nav: true,
            // loop: false
        }
    }
})



var technologyCarousel = $('#Technology');
var technologyItemcount = technologyCarousel.find('.owl-item').length;
technologyCarousel.owlCarousel({
    loop: technologyCarousel > 3,
    // loop: true,
    margin: 54,
    // loop: true,
    autoplay: true,
    smartSpeed: 600,
    autoplay: true,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    nav: true,
    navText: ["<img src='https://rakhospital.com/wp-content/themes/rak-hospital/assets/images/left-chevron.png'>", "<img src='https://rakhospital.com/wp-content/themes/rak-hospital/assets/images/chevron.png'>"],
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: true
        },
        600: {
            items: 2,
            nav: true
        },
        1000: {
            items: 3,
            nav: true,
            // loop: false
        }
    }
})



var doctorCarousel = $('#doctors');
var doctorItemcount = doctorCarousel.find('.owl-item').length;

doctorCarousel.owlCarousel({
    loop: doctorCarousel > 4,
    margin: 54,
    autoplay: false,
    // smartSpeed: 1200,
    // autoplayTimeout: 5000,
    // autoplayHoverPause: true,
    nav: true,
    navText: ["<img src='https://rakhospital.com/wp-content/themes/rak-hospital/assets/images/left-chevron.png'>", "<img src='https://rakhospital.com/wp-content/themes/rak-hospital/assets/images/chevron.png'>"],
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: true
        },
        600: {
            items: 2,
            nav: true
        },
        1000: {
            items: 4,
            nav: true,
            // loop: false
        }
    }
})

$('#servicesec').owlCarousel({
    loop: true,
    margin: 54,
    loop: true,
    autoplay: true,
    smartSpeed: 600,
    autoplay: true,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    nav: true,
    navText: ["<img src='https://rakhospital.com/wp-content/themes/rak-hospital/assets/images/left-chevron.png'>", "<img src='https://rakhospital.com/wp-content/themes/rak-hospital/assets/images/chevron.png'>"],
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: true
        },
        600: {
            items: 2,
            nav: true
        },
        1000: {
            items: 3,
            nav: true,
            // loop: false
        }
    }
})

$('#Testimonials').owlCarousel({
    loop: true,
    margin: 54,
    autoplay: true,
    smartSpeed: 600,
    autoplay: true,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    nav: true,
    navText: ["<img src='https://rakhospital.com/wp-content/themes/rak-hospital/assets/images/left-chevron.png'>", "<img src='https://rakhospital.com/wp-content/themes/rak-hospital/assets/images/chevron.png'>"],
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: true
        },
        600: {
            items: 2,
            nav: true
        },
        1000: {
            items: 4,
            nav: true,
            // loop: false
        }
    }
})

$('#CareSlider').owlCarousel({
    loop: true,
    margin: 54,
    autoplay: true,
    smartSpeed: 600,
    autoplay: true,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    nav: true,
    navText: ["<img src='https://rakhospital.com/wp-content/themes/rak-hospital/assets/images/left-chevron.png'>", "<img src='https://rakhospital.com/wp-content/themes/rak-hospital/assets/images/chevron.png'>"],
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: true
        },
        600: {
            items: 2,
            nav: true
        },
        1000: {
            items: 1,
            nav: true,
            // loop: false
        }
    }
})

$('#countrys').owlCarousel({
    loop: true,
    margin: 30,
    loop: true,
    autoplay: true,
    smartSpeed: 600,
    autoplay: true,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    nav: true,
    navText: ["<img src='https://rakhospital.com/wp-content/themes/rak-hospital/assets/images/left-chevron.png'>", "<img src='https://rakhospital.com/wp-content/themes/rak-hospital/assets/images/chevron.png'>"],
    responsiveClass: true,
    responsive: {
        0: {
            items: 3,
            nav: true
        },
        600: {
            items: 4,
            nav: true
        },
        1000: {
            items: 6,
            nav: true,
            // loop: false
        }
    }
})

document.querySelectorAll('.bodyorgan').forEach(function (bodyorgan) {
    const activeImage = bodyorgan.getAttribute('data-active');
    const inactiveImage = bodyorgan.getAttribute('data-inactive');
    const imgElement = bodyorgan.querySelector('.organ-image');
    const customtooltip = bodyorgan.querySelector('.customtooltip');

    bodyorgan.addEventListener('mouseenter', function () {
        imgElement.src = activeImage; // Show active image
        customtooltip.style.display = 'block'; // Show tooltip
    });

    bodyorgan.addEventListener('mouseleave', function () {
        imgElement.src = inactiveImage; // Show inactive image
        customtooltip.style.display = 'none'; // Hide tooltip
    });
});


$(".heart-set .showSingle").addClass("clicked");
$("#heart-set .organ-tooltip").removeClass("display-none");
autoPlayYouTubeModal();

$(".dropdown-menu.custom-modal-dropdown").on("click", "a", function () {
    var a = $(this).text(),
        t = $(this)[0].parentNode.parentNode.id;

    if (t) {
        $(".dropdown#" + t + " button").text($(this).text());

        if ("truhealth-gender" == t) {
            $(".person-gender").empty();
            $(".person-gender").html(a);

            if ("Female" == a) {
                $("#body-image").attr("src", "your-new-url-path/femalebody.svg");
                $("#body-image").addClass("female-body");
                $(".male_reproductive_system-set").addClass("display-none");
                $(".female_reproductive_system-set").removeClass("display-none");
                selectHeart();
            } else {
                $("#body-image").attr("src", "your-new-url-path/body.svg");
                $("#body-image").removeClass("female-body");
                $(".female_reproductive_system-set").addClass("display-none");
                $(".male_reproductive_system-set").removeClass("display-none");
                selectHeart();
            }
        } else {
            $(".person-age").empty();
            $(".person-age").html(a);
        }
    }
});


// https://rakwithinfinity.online/new/assets/images/svg/body_Male Anatomy.svg

$("#heart-set").find("img").attr("data-src", "https://rakwithinfinity.online/new/assets/images/svg/heart.svg");
$("#heart-set").find("img").addClass("lazyload clicked");

$("#stomach-set.showSingle").click(function () {
    return false;
});

$(".showSingle").click(function () {
    $(".showSingle").each(function () {
        var id = $(this).find("img").attr("id");
        $(this).find("img").attr("src", "https://rakwithinfinity.online/new/assets/images/svg/" + id + "-inactive.svg");
        $(this).find("img").attr("data-src", "https://rakwithinfinity.online/new/assets/images/svg/" + id + "-inactive.svg");
        $(this).find("img").removeClass("clicked");
    });

    var clickedId = $(this).find("img").attr("id");
    $(this).find("img").attr("src", "https://rakwithinfinity.online/new/assets/images/svg/" + clickedId + ".svg");
    $(this).find("img").attr("data-src", "https://rakwithinfinity.online/new/assets/images/svg/" + clickedId + ".svg");
    $(this).find("img").addClass("clicked");
    $(".organ-tooltip").addClass("display-none");
    $(this).find(".organ-tooltip").removeClass("display-none");
    $(".targetDiv").hide();
    $("#details_" + $(this).attr("target")).show();
    $(this).find("img").attr("src", "https://rakwithinfinity.online/new/assets/images/svg/" + $(this).attr("target") + ".svg");

    if ($(this).hasClass("clicked")) {
        $(".showSingle").removeClass("clicked");
    } else {
        $(".showSingle").removeClass("clicked");
        $(this).addClass("clicked");
    }

    if ($(this).hasClass("clicked")) {
        var a = $(this).attr("target");
        $(".showSingle").each(function () {
            if ($(this).attr("target") != a) {
                $(this).find("img").tooltip("hide");
            }
        });
    }

    if ($(window).width() < 768) {
        $("html, body").animate({
            scrollTop: $(".for-phone-scroll").offset().top - 70
        }, "slow");
    }
});

$(".showSingle").mouseover(function () {
    let a = $(this).find("img").attr("id");
    $(this).find("img").attr("src", "https://rakwithinfinity.online/new/assets/images/svg/" + a + ".svg");
    $(this).find("img").attr("data-src", "https://rakwithinfinity.online/new/assets/images/svg/" + a + ".svg");
    $(this).find(".organ-tooltip").removeClass("display-none");
});

$(".showSingle").mouseout(function () {
    let a = $(this).find("img").attr("id");
    if ($(this)[0].className.indexOf("clicked") == -1) {
        $(this).find("img").attr("src", "https://rakwithinfinity.online/new/assets/images/svg/" + a + "-inactive.svg");
        $(this).find("img").attr("data-src", "https://rakwithinfinity.online/new/assets/images/svg/" + a + "-inactive.svg");
        $(this).find(".organ-tooltip").addClass("display-none");
    }
});

$(".organ-issue-btn").click(function () {
    $(".organ-issue-btn").removeClass("active");
    $(this).addClass("active");
});

$(".add-organ-test").click(function () {
    $(".add-organ-test").removeClass("active");
    $(this).addClass("active");
});


$(document).on('click', '[data-lightbox]', function(event) {
    $('body').addClass('no-scroll');
});

$(document).on('click', '.lightboxOverlay', function() {
    $('body').removeClass('no-scroll');
});