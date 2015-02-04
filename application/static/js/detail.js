var $detailModalDialog;

$(document).ready(function(){
    $detailModalDialog = $('#modal-place-detail .modal-dialog');


    $(document).on('click', '[data-target=#modal-place-detail]', function(){

        $detailModalDialog.html('<div style="line-height:200px;" class="modal-loading text-center"><img src="/static/res/img/loading.gif" alt="loading" width="50" height="50"></div>');
        var placeId = $(this).parents('.card').data('placeId');
        getDetailData(placeId);
    });


    $('#modal-place-detail').on('hide.bs.modal', function(){
        reloadCard($(this).find('.modal-content').data('placeId'));
    });


    $(document).on('click', '.btn-load-comments', function(){
        loadComments($(this));
    });

    $(document).on('click', '.btn-like-image:not(.liked)', function(){
        likeImage($(this));
    });



});


function loadComments($target) {
    var placeId = $target.parents('.modal-content').data('placeId');
    var offset = $target.data('offset');

    $target.addClass('disabled');
    $.get('/load_comments/'+placeId+'/'+offset,
        function(response){
            $target.parent()[0].outerHTML = response;
        })
    .always(function(){
        $target.removeClass('disabled');
    });

}

function getDetailData(id) {
    $.get('/get_place_detail/'+id, function(response){
        $detailModalDialog.hide();
        $detailModalDialog.html(response);
        $detailModalDialog.fadeIn('fast');


        $(function () {
            $('#fileupload').fileupload({
                dataType: 'json',
                add: function (e, data) {

                    showToast('업로드 시작...');
                    // reload dialog
                    $detailModalDialog.html('<div style="line-height:200px;" class="modal-loading text-center"><img src="/static/res/img/loading.gif" alt="loading" width="50" height="50"></div><div id="progress"><div class="bar"></div></div>');
                    //$detailModalDialog.html('');

                    data.submit();
                },
                done: function (e, data) {
                    showToast('업로드되었습니다.','success');
                    $('#progress .bar').css('width','0%');
                    
                    
                    getDetailData(id);

                },
                progressall: function (e, data) {
                    var progress = parseInt(data.loaded / data.total * 100, 10);
                    $('#progress .bar').css(
                        'width',
                        progress + '%'
                        );
                }
            });
        });
    });
}

function reloadCard(placeId) {
    if (!placeId) return false;
    var $card = $('.card[data-place-id='+placeId+']');

    $card
    .css('position','relative')
    .append('<div class="mask" style="position: absolute; left: 0px; top: 0px; right: 0px; bottom: 0px; background-color: rgba(0,0,0,0.5); z-index:20;"><img src="/static/res/img/loading.gif" style="position: absolute; display:block; left: 50%; top: 50%; margin-left: -25px; margin-top: -25px;" width="50" height="50"></div>');


    rest({
        target: 'place',
        args: [placeId],
        method: 'GET',
        onsuccess: function(response) {
            //$card[0].outerHTML = response.response;
            var place = Place.fromJsonObject(response.data);
            //$card = place.render();
            $card[0].outerHTML = place.getRenderedHtml();
            placeManager.update(place);
        },
        oncomplete: function() {
            $card.css('position', 'static').find('.mask').remove();
        }
    });
}


function likeImage($clickedBtn) {
    var placeImageId = $clickedBtn.data('placeImageId');

    $clickedBtn.addClass('disabled liked');

    rest({
        target: 'image_like',
        method: 'POST',
        args: [placeImageId],
        onsuccess: function(response) {

            var $count = $clickedBtn.find('.count');
            var likeCount = parseInt($count.text());
            $count.text(likeCount+1);

        },
        onerror: function(jqxhr) {
            switch (jqxhr.status) {
                case 400:
                    showToast('이미 좋아하는 사진이에요', 'warning');
                    break;
                case 401:
                    showToast('로그인 해 주세요', 'warning');
                    break;
                default:
                    showToast('오류가 발생했어요 x_x','error');
                    break;
            }
            $clickedBtn.removeClass('liked');
            return false;
        },
        oncomplete: function() {
            $clickedBtn.removeClass('disabled');
        }


    });
}