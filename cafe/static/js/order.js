let addCartButton = document.querySelectorAll('[id^=addToCart]');
// 장바구니 담기 처리
const addCartButtonClickHandle = (e) =>{
    e.preventDefault();
    
    let id = e.target.id.split("--")[1];
    console.log("add " + id);
    
    // 주문한 상품 총 개수 수정
    var count = document.querySelector("#bar--cart > h2").innerText;
    count *= 1;
    document.querySelector("#bar--cart > h2").innerText = count + 1;

    // 주문 금액 수정
    var price = document.getElementById(id + '--price').innerText.split(' ')[0];
    price *= 1;

    var totalPrice = document.getElementById('total-money').innerText;
    totalPrice *= 1;
    document.getElementById('total-money').innerHTML = (totalPrice + price);
    document.getElementById('cart-total-money').innerHTML = (totalPrice + price) + " 원";


    // 장바구니 담기
    let appendArea = document.getElementById("cart_append_area");
    if (document.getElementById("cart_menu--" + id)){
        let nodeCount =  document.querySelector('#cart_menu--' + id +" p").innerHTML.split(" : ")[1];
        nodeCount *= 1;
        document.querySelector("#cart_menu--"+ id + " > div > div > p").innerHTML = '수량 : ' + (nodeCount + 1);
    }
    else{
        let cloneCartNode = document.getElementById('cart_menu_none').cloneNode(true);
        cloneCartNode.id = "cart_menu--" + id;
        cloneCartNode.style.cssText = "";
        appendArea.append(cloneCartNode);

        console.log(document.querySelector("#cart_menu--" + id.replace(" ", "\\ ") +" > div > img"))
        document.querySelector("#cart_menu--" + id.replace(" ", "\\ ") +" > div > img").src = document.getElementById(id + "--image").src;
        document.querySelector("#cart_menu--" + id.replace(" ", "\\ ") +" > div > div > a > h5").innerHTML = '<strong>' + id + '</strong>';
        document.querySelector("#cart_menu--"+ id.replace(" ", "\\ ") + " > div > div > p").innerHTML = '수량 : 1';
    }

}
for(let i=0;i<addCartButton.length;i++){
    addCartButton[i].addEventListener('click', addCartButtonClickHandle);
}


let tabButton = document.querySelectorAll('[id^=menu_type]');
    
// 음료 카테고리에 따른 탭 메뉴 처리
const tabButtonClickHandle = (e) =>{
    if (e.target !== e.currentTarget) return;
    e.preventDefault();
    
    let id = e.target.id.split("--")[1];
    console.log("selected " + id);
    
    let prevElement = document.querySelector('#drink_tab [class^=on]');
    let prev_id = prevElement.id.split("--")[1];

    $("#menu_type--" + prev_id).removeClass("on");
    $("#menu_content--" + prev_id).hide();
    
    $("#menu_type--" + id).addClass("on");
    $("#menu_content--" + id).show();
}

for(let i=0;i<tabButton.length;i++){
    tabButton[i].addEventListener('click',tabButtonClickHandle);
}


let breadTabButton = document.querySelectorAll('[id^=bread_type]');
    
// 음료 카테고리에 따른 탭 메뉴 처리
const breadTabButtonClickHandle = (e) =>{
    if (e.target !== e.currentTarget) return;
    e.preventDefault();
    
    let id = e.target.id.split("--")[1];
    console.log("selected " + id);
    
    let prevElement = document.querySelector('#bread_tab [class^=on]');
    let prev_id = prevElement.id.split("--")[1];

    $("#bread_type--" + prev_id).removeClass("on");
    $("#bread_content--" + prev_id).hide();
    
    $("#bread_type--" + id).addClass("on");
    $("#bread_content--" + id).show();
}

for(let i=0;i<breadTabButton.length;i++){
    breadTabButton[i].addEventListener('click',breadTabButtonClickHandle);
}

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