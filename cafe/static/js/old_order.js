// GET 방식으로 전송된 데이터 읽기
$.extend({
    getUrlVars: function(){
        var vars = [], hash;
        var hashes = window.location.href.slice(window.location.href.indexOf('?') +1).split('&');
        for(var i = 0; i < hashes.length; i++) {
            hash = hashes[i].split('=');
            vars.push(hash[0]);
            vars[hash[0]] = hash[1];
        }
        console.log(vars);
        return vars;
    }, 
    
    getUrlVar: function(name) {
        return $.getUrlVars()[name];
    }
    
});

document.getElementById("menu_type--bestmenu").innerText = $.getUrlVar('age')+"대" + " 추천 메뉴";


function order_now() {
    let cart_items = document.querySelectorAll('[id^=cart--]');
    if (cart_items.length == 0){
        alert("장바구니가 비어있습니다.");
        return
    }

    let menu_list = new Array();
    let menu_counts = new Array();
    
    for (let i=0;i<cart_items.length;i++){
        var menu_id = cart_items[i].id.split("--")[1];
        var cnt = document.getElementById(menu_id + '--count').innerText * 1; 
        
        console.log(cnt);

        menu_list.push(menu_id);
        menu_counts.push(cnt);
    }
    var usage_type = $.getUrlVar('usage_type');      

    var form = document.getElementById("order_submission");
    var parm = new Array();
    parm.push( ['usage_type', usage_type] );
    parm.push( ['menu_list', menu_list] );
    parm.push( ['menu_counts', menu_counts] );
    parm.push( ['customer_id', $.getUrlVar('customer_id')] );

    var input = new Array();
    for (var i = 0; i < parm.length; i++) {
        input[i] = document.createElement("input");
        input[i].setAttribute("type", "hidden");
        input[i].setAttribute('name', parm[i][0]);
        input[i].setAttribute("value", parm[i][1]);
        form.appendChild(input[i]);
    }
    document.body.appendChild(form);
    form.submit();
}



let tabButton = document.querySelectorAll('[id^=menu_type]');
    
// 음료 카테고리에 따른 탭 메뉴 처리
const tabButtonClickHandle = (e) =>{
    if (e.target !== e.currentTarget) return;
    e.preventDefault();
    
    let id = e.target.id.split("--")[1];
    console.log("selected " + id);
    
    let prevElement = document.querySelector('[class^=on]');
    let prev_id = prevElement.id.split("--")[1];

    $("#menu_type--" + prev_id).removeClass("on");
    $("#menu_content--" + prev_id).hide();
    
    $("#menu_type--" + id).addClass("on");
    $("#menu_content--" + id).show();

}

for(let i=0;i<tabButton.length;i++){
    tabButton[i].addEventListener('click',tabButtonClickHandle);
}

// 장바구니 내에서 음료 개수 추가 (Plus 버튼 클릭)
const addElementButtonClickHandle = (e) =>{
    if (e.target !== e.currentTarget) return;
    e.preventDefault();
    
    console.log(e.target.id);
    let id = e.target.id.split("--")[1];
    console.log("add" + id);

    var prev_count = document.getElementById(id + '--count').innerText;
    prev_count *= 1;
    document.getElementById(id + '--count').innerText = prev_count + 1;

    // 주문한 상품 총 개수 수정
    var count = document.querySelector("#headingOne > button > h4 > sup").innerText;
    count *= 1;
    document.querySelector("#headingOne > button > h4 > sup").innerText = count + 1;

    // 주문 금액 수정
    var price = document.getElementById(id + '--price').innerText.split(' ')[0];
    price *= 1;

    var totalPrice = document.getElementById('total-money').innerText;
    totalPrice *= 1;
    document.getElementById('total-money').innerHTML = '<h5>' + (totalPrice + price) + '</h5>';


}

// 장바구니 내에서 음료 개수 빼기 (Minus 버튼 클릭)
const deductElementButtonClickHandle = (e) =>{
    if (e.target !== e.currentTarget) return;

    e.preventDefault();
    
    console.log(e.target.id);
    let id = e.target.id.split("--")[1];
    console.log("deduct " + id);

    var prev_count = document.getElementById(id + '--count').innerText;
    prev_count *= 1;

    // 1개 남았을 경우, div 삭제
    if (prev_count == 1){
        document.getElementById('cart--' + id).remove();
    } 
    else{
        document.getElementById(id + '--count').innerText = prev_count - 1;
    }
    
    // 주문한 상품 총 개수 수정
    var count = document.querySelector("#headingOne > button > h4 > sup").innerText;
    count *= 1;
    document.querySelector("#headingOne > button > h4 > sup").innerText = count - 1;

    // 주문 금액 수정
    var price = document.getElementById(id + '--price').innerText.split(' ')[0];
    price *= 1;

    var totalPrice = document.getElementById('total-money').innerText;
    totalPrice *= 1;
    document.getElementById('total-money').innerHTML = '<h5>' + (totalPrice - price) + '</h5>';
}



let addCartButton = document.querySelectorAll('[id^=addToCart]');
// 장바구니 담기 처리
const addCartButtonClickHandle = (e) =>{
e.preventDefault();

let id = e.target.id.split("--")[1];
console.log("add " + id);

// 선택한 음료 카테고리가 cart-list에 없는 경우
if (document.getElementById('cart--' + id) == null){
    let cartListArea = document.getElementById('cart-list');
    cartListArea.innerHTML += '<div class="row" id="cart--'+ id +'"> \
                                <div class="col-7" id="cartElement">'+ id +'</div> \
                                <div class="col-1" id="deduct--'+ id +'"><i class="bi bi-dash-circle" style="pointer-events: none;"></i></div> \
                                <div class="col-2" id="'+ id +'--count">1</div> \
                                <div class="col-1" id="add--'+ id +'"><i class="bi bi-plus-circle" style="pointer-events: none;"></i></div> \
                            </div>'
    // Event Listener 추가
    let addElementButton = document.querySelectorAll('[id^=add--]');
    for(let i=0;i<addElementButton.length;i++){
        addElementButton[i].addEventListener('click', addElementButtonClickHandle);
    }
    let deductElementButton = document.querySelectorAll('[id^=deduct--]');
    for(let i=0;i<deductElementButton.length;i++){
        deductElementButton[i].addEventListener('click', deductElementButtonClickHandle);
    }

}else{
    // 선택한 음료 카테고리가 cart-list에 있는 경우, 개수 수정
    var prev_count = document.getElementById(id + '--count').innerText;
    prev_count *= 1;
    document.getElementById(id + '--count').innerText = prev_count + 1;
}

// 주문한 상품 총 개수 수정
var count = document.querySelector("#headingOne > button > h4 > sup").innerText;
count *= 1;
document.querySelector("#headingOne > button > h4 > sup").innerText = count + 1;

// 주문 금액 수정
var price = document.getElementById(id + '--price').innerText.split(' ')[0];
price *= 1;

var totalPrice = document.getElementById('total-money').innerText;
totalPrice *= 1;
document.getElementById('total-money').innerHTML = '<h5>' + (totalPrice + price) + '</h5>';

}
for(let i=0;i<addCartButton.length;i++){
    addCartButton[i].addEventListener('click', addCartButtonClickHandle);
}