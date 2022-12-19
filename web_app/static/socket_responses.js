
// on document ready:
$(document).ready(function () {


  //
  // SOCKETS
  //
 
  socket.on('my_response', function () {
    /**
     * Event handler for new connections.
     * The callback function is invoked when a connection with the
     * server is established.
     */
     console.log('Connected to server');
  });


  socket.on('yt_message', function (msg, cb) {

    /**
     * The youtube demo might take a while to process the video
     * Because of that, we are able to show some messages to the user
     * to let him know what is going on.
     */

    console.log(msg)
    $("#container_result").empty();
    $("#container_result").append("<span><div id='loading' text='" + msg['msg'] + "'></div></span>");


    if (cb)
      cb();
  });


  socket.on('response', function (msg, cb) {

    /**
     * The response from the server 
     */

    // get the frame
    var frame = msg['frame'];

    // create a textarea
    var textarea = document.createElement('textarea');
    textarea.id = 'frame';
    textarea.value = '';
    textarea.spellcheck = false;

    // add the text from the frame to the textarea
    for(var i = 0; i < frame.length; i++) {
      for(var j = 0; j < frame[i].length; j++) {
        textarea.value += frame[i][j];
      }
      textarea.value += '\n'
    }
    
    $("#container_result").empty();
    $("#container_result").append( '<span></span>' );
    $("#container_result > span").append( textarea );

    // adjust the height of the textarea
    textarea.style.height = textarea.scrollHeight + 3+ "px";


  });

});