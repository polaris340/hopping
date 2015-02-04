var Place = function () {
    this.id = null;
    this.name = null;
    this.thumbnailUrl = null;
    this.rateCount = 0;
    this.rateSum = 0;
    this.area = null;
    this.contentType = null;
    this.rated = false;
    this.ratedValue = 0;


    // this.bestComment = {
    //     id:0,
    //     username:null,
    //     body:null
    // };

};




Place.fromJsonObject = function(jsonObject) {
    var place = new Place();
    for (var key in jsonObject) {
        place[key] = jsonObject[key];
    }

    return place;
};

Place.prototype.getDetailData = function() {

}

Place.prototype.rate = function(value) {
    var targetPlace = this;

    // if (targetPlace.removeTimeout) 
    //     clearTimeout(targetPlace.removeTimeout);


    rest({
        target: 'rate',
        method: 'POST',
        args: [targetPlace.id, value],
        onsuccess: function(response) {
            targetPlace.rated = true;
            targetPlace.ratedValue = value;
            targetPlace.rateCount++;
            targetPlace.rateSum += value;


            var $rating = targetPlace.$render().find('.rating');
            $rating.animate({
                opacity:0
            },'fast',function(){
                $rating
                .html(targetPlace.getAverageRateHtml())
                .animate({
                    opacity:1
                },'fast');
            });

            // if (targetPlace.removeTimeout) {
            //     delete targetPlace.removeTimeout;
            // } else {
            //     targetPlace.removeTimeout = setTimeout(function(){
            //         targetPlace.render().fadeOut('slow',function(){

            //             if (window.placeManager) {
            //                 window.placeManager.remove(targetPlace.id);

            //             }
            //         });
            //     }, 2000);
                
            // }


            switch (value) {
                case 1:
                case 2:
                showToast('최악이에요', 'warning');
                break;
                case 3:
                case 4:
                showToast('별로에요', 'warning');
                break;
                case 5:
                case 6:
                showToast('보통이에요');
                break;
                case 7:
                showToast('나쁘지 않아요', 'success');
                break;
                case 8:
                case 9:
                showToast('좋아요!','success');
                break;
                case 10:
                showToast('최고에요!', 'success');
                break;
            }

            //$targetPlaceCard.find('.rating').html(response.response) 
        },
        oncomplete: function() {
            targetPlace
            .$render()
            .find('.rate-area')[0]
            .outerHTML = targetPlace.getRateAreaHtml();
        },
        onerror: function(jqxhr) {
            switch (jqxhr.status) {
                case 400:
                showToast('이미 평가한 장소입니다','warning');
                return false;
            }

            return true;

        }
    });
};

Place.prototype.rateCancel = function() {
    var targetPlace = this;

    // if (targetPlace.removeTimeout) 
    //     clearTimeout(targetPlace.removeTimeout);

    rest({
        target:'rate',
        args: [targetPlace.id],
        method: 'DELETE',
        onsuccess: function(response) {
            targetPlace.rated = false;
            targetPlace.rateCount--;
            targetPlace.rateSum -= targetPlace.ratedValue;
            targetPlace.ratedValue = 0;

            
            // if (targetPlace.removeTimeout) {
            //     delete targetPlace.removeTimeout;
            // } else {
            //     targetPlace.removeTimeout = setTimeout(function(){
            //         targetPlace.render().fadeOut('slow',function(){

            //             if (window.placeManager) {
            //                 window.placeManager.remove(targetPlace.id);

            //             }
            //         });
            //     }, 2000);
                
            // }


            var $rating = targetPlace.$render().find('.rating');
            $rating.animate({
                opacity:0
            },'fast',function(){
                $rating
                .html(targetPlace.getAverageRateHtml())
                .animate({
                    opacity:1
                },'fast');
            });
        },
        oncomplete: function() {
            targetPlace
            .$render()
            .find('.rate-area')[0]
            .outerHTML = targetPlace.getRateAreaHtml();
        }
    });  
};




Place.prototype.update = function(jsonObject) {
    for (var key in jsonObject) {
        this[key] = jsonObject[key];
    }
    this.$render(true);
};

Place.prototype.getAverageRateHtml = function() {
    if (this.rateCount > 0) {
        var averageRate = this.rateSum / this.rateCount / 2;
        var html = '';
        for (var i = 0; i < Math.floor(averageRate); i++) {
            html += '<span class="fa fa-star"></span>';
        }

        if (averageRate - Math.floor(averageRate) > 0.2) {
            html += '<span class="fa fa-star-half"></span>';
        }

        html += ' ' + averageRate.toFixed(1);

        return html;
    } else {
        return '<span class="small">아직 평가가 없어요</span>';
    }
};

Place.prototype.getRateAreaHtml = function () {
    if (this.rated) {// 내가 평가한 경우
        var html = '<div class="panel-footer text-center rate-area rated">';

        for (var i = 0; i < Math.floor(this.ratedValue/2); i++) {
            html += '<span class="fa fa-star active" data-value="'+(i*2+2)+'"></span>';
        }
        if (this.ratedValue%2) {
            html += '<span class="fa fa-star-half-o active" data-value="'+(this.ratedValue+1)+'"></span>';
        }
        for (var i = 0; i<Math.floor( (10-this.ratedValue)/2 ); i++) {
            html += '<span class="fa fa-star-o" data-value="'+( (Math.floor((this.ratedValue+3)/2)+i)*2 )+'"></span>';
        }

        return html;
    } else {
        return '<div class="panel-footer text-center rate-area"><span class="fa fa-star-o" data-value="2"></span><span class="fa fa-star-o" data-value="4"></span><span class="fa fa-star-o" data-value="6"></span><span class="fa fa-star-o" data-value="8"></span><span class="fa fa-star-o" data-value="10"></span></div>';
    }
};

Place.prototype.getBestCommentHtml = function() {
    if (this.bestComment) {
        return '<div class="panel-body best-comment">'
        + '<span class="username small">' + this.bestComment.username + '</span></span>'
        + '<h5 class="text-center">"' + this.bestComment.body + '"</h5>'
        + '</div>';   
    } else {
        return '<div class="panel-body best-comment no-comment">'
        + '<h5 class="text-center">아직 한줄평이 없어요</h5>'
        + '</div>';
    }
}

Place.prototype.$render = function(force) {
    if (typeof force === 'undefined') force = false;

    if (!this.$rendered || force)
        this.$rendered = $(Mustache.render(Place.TEMPLATE, this));

    return this.$rendered;
};

Place.prototype.getRenderedHtml = function() {
    return this.$render()[0].outerHTML;

}


Place.TEMPLATE = /\/\*!?(?:\@preserve)?[ \t]*(?:\r\n|\n)([\s\S]*?)(?:\r\n|\n)\s*\*\//.exec((function () {/*
<div class="card panel panel-default" data-place-id="{{ id }}">
<div class="image-area-wrap">
    <div class="image-area" style="background-image:url('{{ thumbnailUrl }}');">
        <img src="{{ thumbnailUrl }}" alt="{{ name }}">
        <div data-toggle="modal" data-target="#modal-place-detail">

            <div class="description">
                <div class="small">{{ area }} | {{ contentType }}</div>   
                <h4>{{ name }}</h4>
                <div class="rating">
                    {{{ getAverageRateHtml }}}
                </div>
            </div>
        </div>
    </div>
</div>
{{{ getBestCommentHtml }}}
<form class="panel-body comment-form">
    <div class="input-group">
      <input type="text" name="input-comment-body" class="form-control input-sm" placeholder="한줄평을 남겨주세요" required>
      <span class="input-group-btn">
        <button class="btn btn-default btn-sm" type="submit"><span class="glyphicon glyphicon-pencil"></span></button>
    </span>
</div>
</form>
{{{ getRateAreaHtml }}}
</div>
*/}).toString())[1];




