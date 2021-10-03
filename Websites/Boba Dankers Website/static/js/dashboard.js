var socket = io.connect('http://localhost:5000');

function update_dank_data() {
  document.getElementById("colbox1").innerHTML = '<div class = "spinner" style = "font-size: 5px"><div class = "head"></div></div>'
  socket.emit( 'update dank data', {
    id: document.getElementById("id").innerHTML
  })
}

function silent_update_dank_data() {
  socket.emit( 'update dank data', {
    id: document.getElementById("id").innerHTML
  })
}

socket.on( 'dank data return', function( json ) {
  var wallet = json[0];
  var bank = json[1];
  var audio = new Audio("/static?file=mp3/noti.mp3");
  audio.play();
  document.getElementById("colbox1").innerHTML = '<h class="colbox_title">Balance Information</h><br><p class="colbox_text">Wallet: '+wallet.toLocaleString()+'</p><p class="colbox_text">Bank: '+bank.toLocaleString()+'</p>'
})

$(document).ready(function() {
  if (document.getElementById("dankdata").innerHTML === "False") {
    document.getElementById("colbox1").innerHTML = '<div class = "spinner" style = "font-size: 5px"><div class = "head"></div></div>'
    socket.emit( 'update dank data', {
      id: document.getElementById("id").innerHTML
    })
  }
});

window.setInterval(function() {
  silent_update_dank_data()
}, 15000);
