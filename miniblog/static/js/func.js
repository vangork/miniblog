function like(postid) {
    $.get('/like/' + postid,
        function (data, status) {
            if (!data.hasOwnProperty('number')) {
                return false
            }
            $('#post_' + postid + '_like_count').html('<span class="glyphicon glyphicon-heart" aria-hidden="true"></span> ' + data['number']);
            $('#post_' + postid + '_like_count').attr('href', 'javascript:unlike("' + postid + '");');
        }
    );
    return false;
}
function unlike(postid) {
    $.get('/unlike/' + postid,
        function (data, status) {
            if (!data.hasOwnProperty('number')) {
                return false
            }
            $('#post_' + postid + '_like_count').html('<span class="glyphicon glyphicon-heart-empty" aria-hidden="true"></span> ' + data['number']);
            $('#post_' + postid + '_like_count').attr('href', 'javascript:like("' + postid + '");');
        }
    );
    return false;
}