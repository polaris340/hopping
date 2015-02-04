var MAX_VISIBLE_CARDS = 160;
var LIMIT = 8;

$(document).ready(function(){
    initialize();


    
    $(document).on('mouseenter','.card .rate-area:not(.disabled, .rated) span', function(e){
        rateEnter($(this));
    });

    $(document).on('mousemove','.card .rate-area:not(.disabled, .rated) span', function(e){
        rateMove($(this), e);
    });


    $(document).on('mouseleave','.card .rate-area:not(.rated) span', function(){
        rateLeave($(this));
    });


    $(document).on('click','.card .rate-area:not(.disabled) span', function(e){

        if ($(this).parent().hasClass('rated')) {
            cancelRate($(this));
        } else {
            rateEnter($(this));
            rateMove($(this), e);
            rate($(this));
            
        }
    });

    $(document).on('scroll', function(){
        if (!paused 
            && getPlacesXHR.readyState == 4 
            && isScrollBottom()) {
            getPlacesXHR = getPlaces();
    }
});


    $('#btn-load-more').click(function(){
        loadMore(); 
    });


    $('#input-search-keyword').keyup(function(e){
        var keyword = $(this).val();
        if (window.searchXHR) {
            window.searchXHR.abort();
        }
        getPlacesXHR.abort();
        if (keyword == '') {
            paused = false;
            searchResultPlaceManager.removeAll();
            placeManager.showAll();
        } else {
            paused = true;
            placeManager.hideAll();
            searchResultPlaceManager.removeAll();
            
            window.searchXHR = rest({
                target: 'place',
                args: ['search',keyword],
                onsuccess: function(response) {

                    var data = response.data;
                    if (data.length == 0) {
                        showToast('검색 결과가 없습니다');
                        return false;
                    }
                    for (var i = 0; i<data.length; i++) {
                        var place = Place.fromJsonObject(data[i]);
                        place.$render().appendTo($getMinHeightColumn());
                        searchResultPlaceManager.add(place);

                    }

                },
                onerror: function() {
                    return false;
                }
            });
        }
    });


});


function initialize() {
    window.placeManager = new PlaceManager();
    window.searchResultPlaceManager = new PlaceManager();
    window.$columns = $('.column:visible');

    window.getPlacesXHR = false;
    window.$loading = $('#loader');
    window.paused = false;
    getPlacesXHR = getPlaces();

    $('head').append('<style>.card .image-area {min-height:'+$columns.width()+'px;}</style>');
}

function $getMinHeightColumn() {
    var $minHeightColumn = $($columns.get(0));
    var minColumnHeight = $minHeightColumn.height();

    for (var j = 1; j < $columns.length; j++) {
        var $currentColumn = $($columns.get(j));
        if ($currentColumn.height() < minColumnHeight) 
            $minHeightColumn = $currentColumn;

    }

    return $minHeightColumn;
}

function loadMore() {
    $('.card').remove();

    placeManager.nextPage();
    window.paused = false;

    $('#btn-load-more').fadeOut('fast',function(){
        $('#img-loading').fadeIn('fast');
    });
    getPlacesXHR = getPlaces();
}

function isScrollBottom() {
    return ($('body').scrollTop() + $(window).height()) >= $loading.offset().top - 100;
}

function getPlaces() {
    return rest({
        target: 'place',
        args: [placeManager.placeCount() + placeManager.offset, LIMIT],
        method: 'GET',
        onsuccess: function(response) {
            var data = response.data;


            if (data.length == 0) {
                $(document).unbind('scroll');
                $('#img-loading').fadeOut('slow');
            }

            for ( var i = 0; i < data.length; i++ ) {
                var place = Place.fromJsonObject(data[i]);
                placeManager.add(place);
                place.$render().appendTo($getMinHeightColumn());
            }

            if (placeManager.placeCount() >= MAX_VISIBLE_CARDS) {
                // 더 보기 버튼으로 바꾸기
                $('#img-loading').fadeOut('fast',function(){
                    $('#btn-load-more').fadeIn('fast');
                });
                paused = true;
            } else if (isScrollBottom()) {
                getPlacesXHR = getPlaces();
            }
        }

    });
}

function rateEnter($target) {
    var $prev = $target.prevAll();
    $prev.removeClass('fa-star-o fa-star-half-o').addClass('fa-star active');
    $target.addClass('active');
}

function rateLeave($target) {
    var $prev = $target.prevAll();
    $target.removeClass('active').removeClass('fa-star fa-star-half-o').addClass('fa-star-o');
    $prev.removeClass('active').removeClass('fa-star fa-star-half-o').addClass('fa-star-o');


    
}

function rateMove($target, event) {
    $target.removeClass('fa-star-o fa-star-half-o');
    if (event.offsetX > ($target.width()+10)/2) {
        $target.addClass('fa-star');
    } else {
        $target.addClass('fa-star-half-o');
    }
}


function rate($target) {
    var value = parseInt($target.data('value'));
    var $targetPlaceCard = $target.parents('.card');
    var placeId = $targetPlaceCard.data('placeId');

    if ($target.hasClass('fa-star-half-o')) value--;

    $target.parent().addClass('rated');
    $target.parent().addClass('disabled');

    var targetPlace = placeManager.getPlace(placeId) || searchResultPlaceManager.getPlace(placeId);
    targetPlace.rate(value);

    
}

function cancelRate($target) {
    var $targetPlaceCard = $target.parents('.card');
    var placeId = $targetPlaceCard.data('placeId');
    $target.parent().addClass('disabled');

    var targetPlace = placeManager.getPlace(placeId) || searchResultPlaceManager.getPlace(placeId);
    targetPlace.rateCancel();
}

