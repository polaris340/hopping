var PlaceManager = function() {
    this.places = {}; // placeId:place 형태로 저장 
    this.placeIdList = []; // Place 객체의 id를 불러온 순서대로 저장할 배열
    this.offset = 0;
};


PlaceManager.prototype.add = function(newPlace) {
    if (!this.places[newPlace.id]) {
        this.placeIdList.push(newPlace.id);    
    }
    this.places[newPlace.id] = newPlace;
    
};

PlaceManager.prototype.update = function(newPlace) {
    if (this.places[newPlace.id]) {
        this.places[newPlace.id] = newPlace;
    } else {
        this.add(newPlace);
    }
    
};


PlaceManager.prototype.remove = function(placeId) {
    var i = this.placeIdList.indexOf(placeId);

    for (var i = 0; i < this.placeIdList.length; i++) {
        if (this.placeIdList[i] == placeId) break;
    }
    
    if(i < this.placeCount() ) {
        this.placeIdList.splice(i, 1);
        if (this.places[placeId].$rendered)
            this.places[placeId].$rendered.remove();
        delete this.places[placeId];
    }
};

PlaceManager.prototype.getPlace = function(placeId) {
    return this.places[placeId];
};

PlaceManager.prototype.placeCount = function() {
    return this.placeIdList.length;
};

PlaceManager.prototype.clear = function() {
    this.offset = 0;
    this.places = {};
    this.placeIdList = [];
};

PlaceManager.prototype.nextPage = function() {
    this.offset += this.placeCount();
    this.places = {};
    this.placeIdList = [];
};

PlaceManager.prototype.showAll = function() {
    for (var i in this.places) {
        this.places[i].$render().show();
    }
};

PlaceManager.prototype.hideAll = function() {
    for (var i in this.places) {
        this.places[i].$render().hide();
    }
};

PlaceManager.prototype.removeAll = function() {
    for (var i in this.places) {
        this.remove(i);
    }
};


