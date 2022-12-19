////////////////////////
// YouTube - Uploader //
////////////////////////

/**
 * 
 * Get the video id from the url
 * 
 */
function youtube_parser(url) {
    /**
     * Select the id from the url
     * 
     * @param {string} url
     * @return {string} id
     */

    // regex to get the video id
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;

    // get the id
    var match = url.match(regExp);

    // return the id or false
    return (match && match[7].length == 11) ? match[7] : false;
}

function checkThumbnail(width) {
    /**
     * Check if the video is valid, if so, the video should have a valid thumbnail.
     *  
     * @param {int} width
     * @return {boolean}
     *  
     * */

    //HACK a mq thumbnail has width of 320.
    //if the video does not exist(therefore thumbnail don't exist), a default thumbnail of 120 width is returned.
    if (width === 120) {
        //alert("Error: Invalid youtube video");
        console.log("Error: Invalid youtube video")
        $("#container_result").empty();
        $("#container_result").append("<span><div id='error_youtube'>Error: Invalid youtube video</div></span>");
    }
}

function getValidVideoId(url) {
    /**
     * Return a valid video id
     * 
     * @param {string} url
     * @return {string} id
     *  
     **/

    // get the video id from the url
    var id = youtube_parser(url);

    //check if the video id is valid
    var img = new Image();
    img.src = "http://img.youtube.com/vi/" + id + "/mqdefault.jpg";
    img.onload = function () {
        checkThumbnail(this.width);
    }

    // return the id
    return id
}

//
// YouTube - Socket
// 
function youtube() {
    /**
     * Send the video id to the server
     * 
     **/

    // get the raw url
    var url = document.getElementById("youtube");

    // get the video id
    var id = getValidVideoId(url.value);

    // if not false, continue
    if (id === false) {
        return;
    }

    // clean the container
    $("#container_result").empty();
    $("#container_result").append("<span><div id='loading' text='Loading'></div></span>");

    // send the video id to the server
    socket.emit('youtube', { data: id });

}




