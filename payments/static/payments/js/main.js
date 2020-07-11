console.log('check');

fetch("/config/").then((res) => { return res.json(); })
    .then((data) => {
        console.log("data is: ", data);
        const stripe = Stripe(data.public_key);

        document.querySelector('#submitBtn').addEventListener("click", () => {
            fetch("/create-checkout-session/")
                .then((res) => { return res.json(); })
                .then((data) => {
                    console.log(data);
                    return stripe.redirectToCheckout({ sessionId: data.sessionId })
                })
                .then((res) => {
                    console.log(res);
                });
        });
    });