// file dùng để quản lý các chức năng trên trang web liên quan đến carousel (trình chiếu), giỏ hàng (cart), 
// và danh sách yêu thích (wishlist). Cụ thể, các chức năng trong file này bao gồm:
$('#slider1, #slider2, #slider3').owlCarousel({ //mã sử dụng plugin Owl Carousel để thiết lập các trình chiếu
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true
        },
        600: {
            items: 4,
            nav: true,
            autoplay: true
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true
        }
    }
});

// Khi người dùng nhấn vào nút tăng số lượng sản phẩm, hàm AJAX sẽ gửi yêu cầu tới URL /pluscart để cập nhật số lượng sản phẩm trong giỏ hàng. 
// Sau đó, các giá trị về số lượng, tổng số tiền, và tổng số tiền của toàn bộ giỏ hàng sẽ được cập nhật trong giao diện.
$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] 
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})
//khi người dùng nhấn vào nút giảm số lượng, một yêu cầu AJAX được gửi tới URL /minuscart.
// Sau khi dữ liệu được xử lý, số lượng sản phẩm và tổng tiền sẽ được cập nhật trong giao diện.
$('.minus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] 
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})

//Khi người dùng nhấn vào nút xóa sản phẩm khỏi giỏ hàng, yêu cầu AJAX sẽ gửi tới URL /removecart. 
//Sau khi xóa thành công, sản phẩm tương ứng sẽ được xóa khỏi giao diện và tổng số tiền cũng sẽ được cập nhật.
$('.remove-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove() 
        }
    })
})

// Khi nhấn vào nút thêm vào wishlist, AJAX gửi yêu cầu tới /pluswishlist. 
//Sau khi hoàn thành, trang sẽ tự động chuyển hướng tới trang chi tiết sản phẩm với ID tương ứng.
$('.plus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/pluswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            //alert(data.message)
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})

//Khi nhấn vào nút xóa khỏi wishlist, AJAX gửi yêu cầu tới /minuswishlist. 
//Sau đó, trang sẽ chuyển hướng tới trang chi tiết sản phẩm tương ứng.
$('.minus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/minuswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})
