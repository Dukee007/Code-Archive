//                                                     COOKIE MESSAGE DISPLAY

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

$(document).ready(function() {
  if (getCookie("cookie_msg") != "false") {
    var el = document.getElementById("cookie");
    el.style.display = "flex";
  }
});

function close_cookie_message() {
  var el = document.getElementById("cookie");
  el.style.display = "none";
  document.cookie = "cookie_msg=false";
}
