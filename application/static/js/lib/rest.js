/*
target : table name
method : GET, POST, PUT, DELETE
args : url parameters as array
data : javascript object,

onsuccess, onerror, oncomplete
*/


function rest(option) {


    var url = "/"+option.target;

    if (option.args) {

        for (var i = 0; i < option.args.length; i++) {
            url += '/'+option.args[i];
        }
    }

    var ajaxOption = {
        url:url,
        type: option.method,
        dataType: 'json',
        contentType: 'application/json',
        success: function(response) {


            if (option.onsuccess) {
                if (!option.onsuccess(response)) return false;
            }
        },
        error: function(jqxhr) {


            if (option.onerror) {
                if (!option.onerror(jqxhr)) return false;
            }

            switch (jqxhr.status) {
                case 401:
                showToast('로그인이 필요합니다.', 'warning');
                break;
                default:
                showToast('오류가 발생했습니다. 잠시 후에 다시 시도해주세요', 'error');
                break;
            }

            

        },
        complete: function() {
            if (option.oncomplete) {
                if (!option.oncomplete()) return false;
            }
        }

    };

    if (option.data) {
        ajaxOption.data = JSON.stringify(option.data);
    }

    return $.ajax(ajaxOption);
}