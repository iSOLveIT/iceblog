// JQuery for Likes
$(function(){
    // Like button event
    $(".btn_like").bind('click', function(){
        // Declare variables and assign value to them
        var blogID = $(".btn_like").attr("id");
        var noLikes = $(".btn_like").attr("value");
        var noLikes = parseInt(noLikes);

        // Check if the button is clicked or not
        if (noLikes === 1){
            // Send json data and store the response
            $.getJSON($SCRIPT_ROOT + '/likes', {blog_id: blogID, no_likes: noLikes},
            function(data){
                $("#current_like").text(data.result);
            });
            $('#user_like').removeClass('dislike');
            $('#user_like').addClass('like');
            $('.btn_like').addClass('jump');
            $('.btn_like').val('-1'); 
        }    
        else{
            // Send json data and store the response
            $.getJSON($SCRIPT_ROOT + '/likes', {blog_id: blogID, no_likes: noLikes},
            function(data){
                $("#current_like").text(data.result);
            });
            $('#user_like').removeClass('like');
            $('#user_like').addClass('dislike');
            $('.btn_like').removeClass('jump');
            $('.btn_like').val('+1');        
        }
    });
});