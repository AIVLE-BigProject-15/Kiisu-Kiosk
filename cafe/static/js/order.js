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

document.getElementById("menu_type--bestmenu").innerText = "BEST FOR " + $.getUrlVar('age')+"'s";
if ($.getUrlVar('confidence') >= 0.5){
    $("#alert_for_low_confidence").hide();
}


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





function go_pay() {
    setTimeout(pay_now, 5000);
};
function pay_now() { 
    var form = document.getElementById("order_submission");
    var parm = new Array();

    var menus = new Array();
    var counts = new Array();
    var cart_menus = document.querySelectorAll("[id^=cart_menu--]")
    for (let i=0; i < cart_menus.length; i++){
        var id = cart_menus[i].id.split("--")[1]
        menus.push(id);
        counts.push(document.querySelector("#cart_menu--"+ id.replace(" ", "\\ ") + " > div > div > p").innerHTML.split(': ')[1]);
    }
    console.log(menus, counts)
    parm.push( ['usage_type', $.getUrlVar('usage_type')] );
    parm.push( ['menu_list', menus] );
    parm.push( ['menu_counts', counts] );
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