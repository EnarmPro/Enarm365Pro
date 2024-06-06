(function() {
    // Evita la ejecución múltiple
    if (window.paypalScriptLoaded) {
        return;
    }
    window.paypalScriptLoaded = true;

    // Función para obtener el token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    window.paypal.Buttons({
        style: {
            shape: 'rect',
            layout: 'vertical',
        },
        createOrder: async function(data, actions) {
            try {
                const response = await fetch("/create_order", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                        cart: [
                            {
                                id: "YOUR_PRODUCT_ID",
                                quantity: "YOUR_PRODUCT_QUANTITY",
                            },
                        ],
                    }),
                });

                const orderData = await response.json();

                if (orderData.id) {
                    return orderData.id;
                } else {
                    const errorDetail = orderData?.details?.[0];
                    const errorMessage = errorDetail
                        ? `${errorDetail.issue} ${errorDetail.description} (${orderData.debug_id})`
                        : JSON.stringify(orderData);

                    throw new Error(errorMessage);
                }
            } catch (error) {
                console.error(error);
                resultMessage(`Could not initiate PayPal Checkout...<br><br>${error}`);
            }
        },
        onApprove: async function(data, actions) {
            try {
                const response = await fetch(`/orders/${data.orderID}/capture`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        'X-CSRFToken': csrftoken
                    },
                });

                const orderData = await response.json();
                const errorDetail = orderData?.details?.[0];

                if (errorDetail?.issue === "INSTRUMENT_DECLINED") {
                    return actions.restart();
                } else if (errorDetail) {
                    throw new Error(`${errorDetail.description} (${orderData.debug_id})`);
                } else if (!orderData.purchase_units) {
                    throw new Error(JSON.stringify(orderData));
                } else {
                    const transaction = orderData.purchase_units[0].payments.captures[0] ||
                                        orderData.purchase_units[0].payments.authorizations[0];
                    resultMessage(
                        `Transaction ${transaction.status}: ${transaction.id}<br><br>See console for all available details`,
                    );
                    console.log("Capture result", orderData, JSON.stringify(orderData, null, 2));
                }
            } catch (error) {
                console.error(error);
                resultMessage(`Sorry, your transaction could not be processed...<br><br>${error}`);
            }
        },
    }).render("#paypal-button-container");

    function resultMessage(message) {
        const container = document.querySelector("#result-message");
        container.innerHTML = message;
    }
})();