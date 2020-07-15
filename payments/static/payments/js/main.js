let stripe = null;

fetch("/config/").then((res) => { return res.json(); })
    .then((data) => {
        stripe = Stripe(data.public_key);
    });

//     document.querySelector('#submitBtn').addEventListener("click", () => {
//     fetch("/create-checkout-session/")
//         .then((res) => { return res.json(); })
//         .then((data) => {
//             console.log(data);
//             return stripe.redirectToCheckout({ sessionId: data.sessionId })
//         })
//         .then((res) => {
//             console.log(res);
//         });
// });
// });

// document.getElementById('dono_form').addEventListener('submit', (event) => {
//     event.preventDefault();

//     console.log("clicked");
//     console.log(JSON.stringify(Object.fromEntries(new FormData(event.target))));
// fetch('/create-checkout-session/', {
//     method: 'POST',
//     data: JSON.stringify(Object.fromEntries(new FormData(event.target)))
// }).then((res) => { return res.json(); })
//     .then((data) => {
//         console.log(data);
//         return stripe.redirectToCheckout({ sessionId: data.sessionId })
//     })
//     .then((res) => {
//         console.log(res);
//     });
// });

$(document).ready(function () {
    $('#dono_form').submit(function (e) {
        e.preventDefault();
        $.ajax({
            data: $(this).serialize(),
            type: 'post',
            url: '/create-checkout-session/',
            contentType: "application/x-www-form-urlencoded",
            success: function (res) {
                console.log(res);
                return stripe.redirectToCheckout({ sessionId: res.sessionId });
            },
            error: function (err) {
                console.log(err);
            }
        });
    });
});