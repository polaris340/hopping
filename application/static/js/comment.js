$(document).ready(function(){
    $(document).on('submit','form.comment-form', function(){
        onCommentFormSubmit($(this));
        return false;
    });

    $(document).on('click', '.btn-like', function(){
        if ($(this).hasClass('liked')) {
            likeCommentCancel($(this));
        } else {
            likeComment($(this));
        }
    });

    $(document).on('click', '.btn-delete-comment', function(){
        deleteComment($(this));
    });
});

function deleteComment($target) {
    var targetCommentId = $target.data('targetCommentId');

    $target.addClass('disabled');
    rest({
        target: 'comment',
        method: 'DELETE',
        args:[targetCommentId],
        onsuccess:function(response) {
            $target.parents('.modal-content')[0].outerHTML = response.response;
        },
        onerror:function(jqxhr) {

        },
        oncomplete: function() {
            $target.removeClass('disabled');
        }
    });
}

function likeComment($target) {
    var targetCommentId = $target.data('targetCommentId');

    $target.addClass('disabled');
    $target.addClass('liked');
    rest({
        target: 'comment_like',
        method: 'POST',
        args: [targetCommentId],
        onsuccess:function(response) {

            $target.find('.count').text(response.response);
            
        },
        onerror:function(jqxhr) {
            
            $target.removeClass('liked');
            switch (jqxhr.status) {
                case 400:
                if (jqxhr.responseJSON.code == 400001)
                    showToast('이미 좋아하고 있어요','warning');
                else if (jqxhr.responseJSON.code == 400002)
                    showToast('당신 댓글에 좋아요를 누르는건 좀...','warning');
                return false;

            }
            return true;
        },
        oncomplete:function(){
            $target.removeClass('disabled');
        }
        
    });
}

function likeCommentCancel($target) {
    var targetCommentId = $target.data('targetCommentId');

    $target.addClass('disabled');
    $target.removeClass('liked');
    rest({
        target: 'comment_like',
        method: 'DELETE',
        args: [targetCommentId],
        onsuccess:function(response) {
            $target.find('.count').text(response.response);
        },
        onerror:function(jqxhr) {
            $target.addClass('liked');
            switch (jqxhr.status) {
                case 404:
                showToast('좋아하는 한줄평이 아니에요','warning');
                return false;

            }
            return true;
        },
        oncomplete:function(){
            
            $target.removeClass('disabled');
        }
    });
}

function onCommentFormSubmit($targetForm) {
    var $commentInput = $targetForm.find('input[name=input-comment-body]');
    var $submitBtn = $targetForm.find('button');
    var $targetPlaceCard = $targetForm.parents('.card');
    var placeId = $targetPlaceCard.data('placeId');

    if ($commentInput.val().trim() == '') {
        $commentInput.select();
        showToast('내용을 입력해주세요','warning');
        return false;
    }

    var data = {
        body:$commentInput.val()
    };

    $commentInput.attr('disabled','disabled');
    $submitBtn.attr('disabled','disabled');

    rest({
        target: 'comment',
        method: 'POST',
        args: [placeId],
        data: data,
        onsuccess: function(response) {
            showToast('등록되었습니다', 'success');
            $bestCommentArea = $targetPlaceCard.find('.best-comment');
            if ($bestCommentArea.hasClass('no-comment')) {
                $bestCommentArea.animate({
                    opacity:0
                },'fast',function(){
                    $bestCommentArea
                    .removeClass('no-comment')
                    .html(response.response)
                    .animate({
                        opacity:1
                    },'fast');
                });


                //$bestCommentArea.removeClass('no-comment').html(response.response);
            }
            $commentInput.val('');
        },
        oncomplete: function() {
            $commentInput.removeAttr('disabled');
            $submitBtn.removeAttr('disabled');
        },
        onerror: function(jqxhr) {
            switch (jqxhr.status) {
                case 400:
                showToast('내용을 입력해주세요','warning');
                break;
                case 401:
                showToast('로그인이 필요합니다','warning');
                break;
            }
        }
    });
}