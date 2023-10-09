function sendMessage() {
    const csrfToken = $('meta[name="csrf-token"]').attr('content');
    const URL = "http://127.0.0.1:8888/mess/chat/send_mess/";
    let mess_text = $('#chat-input').val();
    let initiator_var = $('#chat-input').data("initiator");
    let companion_var = $('#chat-input').data('companion');
    $.ajax({
        url: URL,
        type: 'POST',
        cache: false,
        data: {
            csrfmiddlewaretoken: csrfToken,
            companion: companion_var,
            initiator: initiator_var,
        },
        success: function (responce){
            console.log($('#responce').text(responce.message));
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + xhr.responceText);
        }
    },
        )
}
