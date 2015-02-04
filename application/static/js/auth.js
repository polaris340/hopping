var PATTERN_EMAIL = /^([0-9a-zA-Z_]([-._\w]*[0-9a-zA-Z])*@([0-9a-zA-Z][-\w]*[0-9a-zA-Z]\.)+[a-zA-Z]{2,9})$/;

$(document).ready(function(){
    $('#form-signup #input-email').change(function(){
        var email = $(this).val();
        if (email != '')
            emailDuplicateCheck($(this));
    });

    $('#form-signup #input-password').change(function(){
        var password = $(this).val();
        if (password.length < 6 || password.legnth > 20) {
            showToast('비밀번호는 6~20자로 입력해주세요', 'warning');
            $(this).addClass('error');
            $(this).focus();
            return false;
        } else {
            $(this).removeClass('error');
        }
    });
    $('#form-signup #input-password-confirm').change(function(){
        var password = $('#form-signup #input-password').val();
        var passwordConfirm = $(this).val();

        if (password != passwordConfirm) {
            showToast('비밀번호가 일치하지 않습니다', 'warning');
            $(this).addClass('error');
            $(this).focus();
            return false;
        } else {
            $(this).removeClass('error');
        }
    });

    $('#form-signup').submit(function(){
        if ($(this).find('.form-control.error').length > 0) {
            showToast('입력한 내용에 오류가 있습니다','warning');
            return false;
        }
    });

});


function emailDuplicateCheck($emailInput) {
    var email = $emailInput.val();
    
    if (!email.match(PATTERN_EMAIL)) {
        showToast('이메일 형식에 맞게 입력해주세요','warning');
        $emailInput.addClass('error');
        $emailInput.focus();
        return false;
    } else {
        $emailInput.removeClass('error');
    }

    $.post('/email_check', {email:email}, function(){
        $emailInput.removeClass('error');
    }).fail(function(jqxhr){
        //if check failed
        switch(jqxhr.status) {
            case 400:
                showToast('사용중인 이메일 주소입니다.', 'warning');
                $emailInput.addClass('error');
                break;
            default:
                showToast('오류가 발생했습니다. 잠시 후에 다시 시도해주세요', 'error');
                break;

            $emailInput.focus();
        }
    });
}

