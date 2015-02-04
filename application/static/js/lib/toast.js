var color = {
    'default':'#28324E',
    warning:'#f37934',
    error:'#b8312f',
    success:'#2969b0'
};

var defaultStyle = {
    color:'white',
    display:'inline-block',
    borderRadius:'.5em',    
    lineHeight:'1.8em',
    fontWeight:'bold',
    fontSize:'1.2em',
    padding:'0px 10px'

};

function showToast(message, level, style){

    level = level || 'default';

    // set custom styles
    if(style){
        for(s in defaultStyle){
            if(!style[s]){
                style[s] = defaultStyle[s];
            }
        }
    }else{
        style = defaultStyle;
    }

    style.backgroundColor = color[level];
    


    if($('div#toast').length>0){
        setTimeout('showToast("'+message+'","'+level+'", '+JSON.stringify(style)+')',300);
    }else{
        var toast = '<div id="toast" style="text-align:center;position:fixed;bottom:20%;width:100%;padding:0px;maring:0px;display:none;z-index:9999;"><span>'+message+'</span></div>';
        
        $('body').append(toast);
        $('div#toast')
            .find('span')
            .css(style)
            .parent()
            .fadeIn(300)
            .delay(1000)
            .fadeOut(300,function(){

                $('div#toast').remove();
            }); 
    }
    

}


