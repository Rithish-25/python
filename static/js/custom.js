$(document).ready(function () {

    // Increment quantity
    $('.increment-btn').click(function (e) {
        e.preventDefault();
        var qtyInput = $(this).closest('.product_data').find('.qty-input');
        var value = parseInt(qtyInput.val(), 10);
        value = isNaN(value) ? 0 : value;
        if (value < 10) {
            value++;
            qtyInput.val(value);
        }
    });

    // Decrement quantity
    $('.decrement-btn').click(function (e) {
        e.preventDefault();
        var qtyInput = $(this).closest('.product_data').find('.qty-input');
        var value = parseInt(qtyInput.val(), 10);
        value = isNaN(value) ? 0 : value;
        if (value > 1) {
            value--;
            qtyInput.val(value);
        }
    });

    // Add to cart
    $('.addToCartBtn').click(function (e) {
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: '/add-to-cart',
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            dataType: 'json',
            success: function (response) {
                alertify.success(response.status);
            },
            error: function (xhr, status, error) {
                alertify.error("An error occurred: " + error);
            }
        });
    });


    $('.addToWishlist').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/add-to-wishlist",
            data: {
                "product_id": product_id,
            
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status);
            }
        });
    });



    



    // Update quantity in cart
    $('.changeQuantity').click(function (e) {
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/upadte-cart",
            data: {
                "product_id": product_id,
                "product_qty": product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status);
            }
        });
    });

    // Delete item from cart
    $(document).on('click','.delete-cart-item',function (e) {
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/delete-cart-item",
            data: {
                "product_id": product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status);
                $('.cartdata').load(location.href + " .cartdata");
            }
        });
    });

    $(document).on('click', '.delete-wishlist-item', function (e) {
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
    
        $.ajax({
            method: "POST",
            url: "/delete-wishlist-item",
            data: {
                "product_id": product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status);
                // Optional: Refresh page or remove item from DOM
                location.reload(); 
            },
            error: function () {
                alertify.error("Something went wrong!");
            }
        });
    });
    

});
